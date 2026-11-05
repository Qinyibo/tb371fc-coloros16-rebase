"""Describe a fixed third-party replay; do not infer user acceptance from metrics."""
import argparse,csv,json,re,subprocess
from decimal import Decimal
from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--work',required=True,type=Path);args=p.parse_args()
w=(r/args.work).resolve();assert w.is_relative_to(r)
text=(w/'workload.txt').read_text();stamps=re.findall(r'^(\d+\.\d+) \d+\.\d+$',text,re.M);assert len(stamps)==2
start,end=[int(Decimal(s)*10**9) for s in stamps]
counts={app:len(re.findall(r'^Starting: Intent .* cmp='+re.escape(app)+r'/',text,re.M)) for app in ['com.ss.android.ugc.aweme','com.luna.music']}
assert all(n==8 for n in counts.values()),counts
sql=f'''
CREATE PERFETTO TABLE w AS SELECT {start} AS ws,{end} AS we;
INCLUDE PERFETTO MODULE android.binder;
SELECT ws/1e9 AS start_s,we/1e9 AS end_s,(we-ws)/1e9 AS workload_s,start_ts<=ws AND end_ts>=we AS complete_trace_coverage FROM trace_bounds CROSS JOIN w;
CREATE PERFETTO TABLE frames AS
SELECT CASE WHEN f.layer_name LIKE '%com.ss.android.ugc.aweme/%' THEN 'com.ss.android.ugc.aweme'
WHEN f.layer_name LIKE '%com.luna.music/%' THEN 'com.luna.music' ELSE p.name END AS app,
f.upid,f.surface_frame_token,MAX(f.dur) AS dur,
MAX(f.jank_type GLOB '*App Deadline Missed*') AS app_missed,
MAX(f.present_type='Late Present') AS late
FROM actual_frame_timeline_slice f JOIN process p USING(upid) CROSS JOIN w
WHERE f.ts>=ws AND f.ts+f.dur<=we AND f.dur>0 AND f.surface_frame_token>0
GROUP BY app,f.upid,f.surface_frame_token;
SELECT app,COUNT(*) AS unique_surface_tokens,ROUND(PERCENTILE(dur,50)/1e6,2) AS p50_ms,ROUND(PERCENTILE(dur,95)/1e6,2) AS p95_ms,ROUND(MAX(dur)/1e6,2) AS max_ms,SUM(app_missed) AS missed,SUM(late) AS late
FROM frames WHERE app IN ('com.android.launcher','com.android.systemui','com.ss.android.ugc.aweme','com.luna.music') GROUP BY app;
SELECT COUNT(*) AS waits,ROUND(PERCENTILE(s.dur,95)/1e6,2) AS p95_ms,ROUND(MAX(s.dur)/1e6,2) AS max_ms,SUM(s.dur>10000000) AS waits_over_10ms
FROM slice s JOIN thread_track tt ON s.track_id=tt.id JOIN thread t USING(utid) JOIN process p USING(upid) CROSS JOIN w
WHERE s.ts>=ws AND s.ts+s.dur<=we AND p.name='/system/bin/surfaceflinger' AND t.name='RE Completion' AND s.name='waitForever';
SELECT p.name,ROUND(SUM(MIN(s.ts+s.dur,we)-MAX(s.ts,ws))/1e6,2) AS cpu_ms
FROM sched s JOIN thread t USING(utid) LEFT JOIN process p USING(upid) CROSS JOIN w
WHERE s.ts<we AND s.ts+s.dur>ws AND s.dur>0 AND s.utid!=0 GROUP BY p.upid ORDER BY cpu_ms DESC LIMIT 15;
SELECT b.client_thread,COUNT(*) AS calls,ROUND(PERCENTILE(b.client_dur,95)/1e6,2) AS p95_ms,ROUND(MAX(b.client_dur)/1e6,2) AS max_ms
FROM android_binder_txns b CROSS JOIN w WHERE b.client_ts>=ws AND b.client_ts+b.client_dur<=we AND b.is_sync AND b.client_process='com.android.launcher' GROUP BY b.client_thread ORDER BY max_ms DESC LIMIT 8;
SELECT name,value FROM stats WHERE value>0 AND (name GLOB '*lost*' OR name GLOB '*overrun*' OR name GLOB '*overwrite*');
'''
(w/'metrics.sql').write_text(sql,encoding='utf8')
x=subprocess.run([str(r/'tools/trace_processor_shell.exe'),'query','--format','csv','--quiet','-f',str(w/'metrics.sql'),str(w/'capture/heavy.pftrace')],capture_output=True,timeout=70)
(w/'metrics.txt').write_bytes(x.stdout);(w/'analysis-stderr.txt').write_bytes(x.stderr);assert x.returncode==0,x.stderr.decode(errors='replace')
tables=x.stdout.decode().replace('\r','').strip().split('\n\n');coverage=next(csv.DictReader(tables[0].splitlines()));assert coverage['complete_trace_coverage']=='1',coverage
frame_rows=list(csv.DictReader(tables[1].splitlines()));have={row['app'] for row in frame_rows if int(row['unique_surface_tokens'])>0}
qualified={'com.ss.android.ugc.aweme','com.luna.music'}<=have
snapshot_before=(w/'capture/capture-start-state.txt').read_text().replace('\r','').splitlines();snapshot_after=(w/'capture/capture-end-state.txt').read_text().replace('\r','').splitlines()
epoch0,epoch1=float(snapshot_before[2]),float(snapshot_after[2]);events=[]
for line in (w/'capture/process-events.log').read_text(errors='replace').splitlines():
 m=re.match(r'^\s*(\d+\.\d+)',line)
 if m and epoch0<=float(m.group(1))<=epoch1 and re.search(r'\b(am_kill|am_proc_start|am_proc_died|am_freeze|am_unfreeze)\b',line):events.append(line)
(w/'timed-process-events.txt').write_text('\n'.join(events)+'\n',encoding='utf8')
result={'explicit_launches':counts,'trace_covers_workload':True,'both_third_party_apps_rendered':qualified,'boot_id_unchanged':snapshot_before[1]==snapshot_after[1],'gpu_level_start':snapshot_before[3],'gpu_level_end':snapshot_after[3],'lifecycle_events_in_capture':len(events),'user_acceptance':False,'performance_gain_verified':False}
(w/'qualification.json').write_text(json.dumps(result,indent=2)+'\n');print(x.stdout.decode());print(json.dumps(result),flush=True)
