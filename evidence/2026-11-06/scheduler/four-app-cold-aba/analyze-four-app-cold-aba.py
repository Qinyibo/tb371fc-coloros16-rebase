from pathlib import Path
import argparse, csv, io, json, re, subprocess
from decimal import Decimal
from statistics import median

parser = argparse.ArgumentParser()
parser.add_argument('work', type=Path)
args = parser.parse_args()
work = args.work.resolve()
root = Path.cwd()
assert work.is_relative_to(root)
processor = root/'tools/trace_processor_shell.exe'


def marker(text, name):
    value = re.search(rf'^{name} (\d+\.\d+)', text, re.M)
    assert value, name
    return int(Decimal(value[1])*10**9)


def parse_round(text):
    visits=[]
    for match in re.finditer(r'^APP (\d+) ([\w.]+)\n(.*?)(?=^APP |^WINDOW_END |\Z)',text,re.M|re.S):
        cycle, app, item = match.groups()
        def get(p):
            m=re.search(p,item,re.M)
            return m[1] if m else None
        cold=get(r'^LaunchState: (\w+)')
        visits.append({'cycle':int(cycle),'app':app,'launch_state':cold,'reported_ok':bool(re.search(r'^Status: ok$',item,re.M)),
           'launch_ms':int(get(r'^TotalTime: (\d+)')) if get(r'^TotalTime: (\d+)') else None,
           'focus':get(r'mCurrentFocus=Window\{[^ ]+ u\d+ (\S+?)\}'),
           'scheduler':get(r'^STATE (\w+)'),'tune':get(r'^TUNE (\d+ \d+ \d+)'),
           'thermal_mC':list(map(int,get(r'^THERMAL (\d+ \d+ \d+)').split())),
           'battery_dC':int(get(r'^\s*temperature: (\d+)')),
           'refresh_hz':float(get(r'peakRefreshRate=([\d.]+)')),
           'vsync_hz':float(get(r'vsyncRate=([\d.]+)')),
           'bounds_px':[int(get(r'DisplayMode\{[^\n]*?width=(\d+)')),int(get(r'DisplayMode\{[^\n]*?height=(\d+)'))],
           'begin_ns':marker(item,'LAUNCH_BEGIN'),'swipe_ns':marker(item,'SWIPE_BEGIN'),'end_ns':marker(item,'APP_END')})
    return visits


records={}
for phase in ['A1','B','A2']:
    folder = work/phase
    trace = folder/'heavy.pftrace'
    if not trace.exists() or trace.stat().st_size<100000 or not (folder/'events.txt').exists():
        continue
    raw=(folder/'workload.txt').read_text(encoding='utf-8')
    runs=parse_round(raw)
    warm=parse_round((folder/'warmup.txt').read_text(encoding='utf-8'))
    assert len(runs)==8 and len(warm)==4
    tuples=',\n'.join(f"({i},'{r['app']}',{r['begin_ns']},{r['swipe_ns']},{r['end_ns']})" for i,r in enumerate(runs))
    sql=f'''CREATE PERFETTO TABLE visits AS WITH v(idx, app, launch_ns, swipe_ns, end_ns) AS (VALUES {tuples}) SELECT * FROM v;
CREATE PERFETTO TABLE matched_frames AS
SELECT v.idx, f.upid, f.surface_frame_token, MIN(f.ts) AS ts, MAX(f.dur) AS dur,
 MAX(f.jank_type GLOB '*App Deadline Missed*') AS missed,
 MAX(f.present_type = 'Late Present') AS late
FROM visits v JOIN actual_frame_timeline_slice f ON f.ts>=v.launch_ns AND f.ts+f.dur<=v.end_ns
JOIN process p USING(upid)
WHERE f.dur>0 AND f.surface_frame_token>0 AND (p.name=v.app OR f.layer_name LIKE '%'||v.app||'/%')
GROUP BY v.idx, f.upid, f.surface_frame_token;
SELECT start_ts<={marker(raw,'WINDOW_BEGIN')} AND end_ts>={marker(raw,'WINDOW_END')} AS coverage FROM trace_bounds;
SELECT v.idx, v.app, COUNT(f.dur) AS frames, ROUND(PERCENTILE(f.dur,95)/1e6,2) AS p95_ms,
 SUM(f.missed) AS app_missed,SUM(f.late) AS late, SUM(f.ts>=v.swipe_ns) AS frames_after_swipe,
 ROUND(MIN(CASE WHEN f.ts>=v.swipe_ns THEN f.ts+f.dur-v.swipe_ns END)/1e6,2) AS first_frame_end_after_swipe_marker_ms
FROM visits v LEFT JOIN matched_frames f USING(idx) GROUP BY v.idx,v.app ORDER BY v.idx;
SELECT ts-clock_value AS monotonic_to_boottime_ns FROM clock_snapshot WHERE clock_name='MONOTONIC' LIMIT 1;
SELECT name,value FROM stats WHERE value>0 AND (name GLOB '*lost*' OR name GLOB '*overrun*' OR name GLOB '*overwrite*');
'''
    query=folder/'metrics.sql';query.write_text(sql,encoding='utf-8',newline='\n')
    result=subprocess.run([str(processor),'query','--format','csv','--quiet','-f',str(query),str(trace)],capture_output=True,timeout=80,check=True)
    (folder/'metrics.txt').write_bytes(result.stdout)
    output=result.stdout.decode().replace('\r','').strip().split('\n\n')
    coverage=next(csv.DictReader(io.StringIO(output[0])))['coverage']=='1'
    metrics=list(csv.DictReader(io.StringIO(output[1])))
    assert len(metrics)==len(runs)
    for visit, frames in zip(runs,metrics,strict=True):
        assert visit['app']==frames['app']
        visit['frame_timeline']=frames
    expected='stopped' if phase=='B' else 'running'
    tune=('0','0') if phase=='B' else ('30','1')
    tune_valid=all(v['scheduler']==expected and tuple(v['tune'].split()[:2])==tune and (int(v['tune'].split()[2])==0 if phase=='B' else int(v['tune'].split()[2])>0) for v in warm+runs)
    offset=int(next(csv.DictReader(io.StringIO(output[2])))['monotonic_to_boottime_ns'])
    events=[]
    for line in (folder/'events.txt').read_text(errors='replace').splitlines():
        stamp=re.match(r'^\s*\[?\s*(\d+\.\d+)',line)
        if not stamp:continue
        time=int(Decimal(stamp[1])*10**9)+offset
        if marker(raw,'WINDOW_BEGIN')<=time<=marker(raw,'WINDOW_END') and any(v['app'] in line for v in runs):events.append(line)
    records[phase]={'trace_coverage':coverage,'tune_valid':tune_valid,'warmup_all_four_cold':all(v['launch_state']=='COLD' and v['reported_ok'] for v in warm),
       'measured_all_eight_cold':all(v['launch_state']=='COLD' and v['reported_ok'] for v in runs),
       'focus_login_seen':sorted({v['app'] for v in runs if v['focus'] and re.search('login|auth',v['focus'],re.I)}),
       'refresh_hz':sorted({v['refresh_hz'] for v in runs}),'battery_c':sorted({v['battery_dC']/10 for v in runs}),
       'thermal_ranges_c':[(min(v['thermal_mC'][i] for v in runs)/1000,max(v['thermal_mC'][i] for v in runs)/1000) for i in range(3)],
       'target_lifecycle_events':events,'trace_loss_rows':output[3:] ,'visits':runs}
    print(phase,{k:v for k,v in records[phase].items() if k not in ('visits','target_lifecycle_events')})
    for app in dict.fromkeys(v['app'] for v in runs):
        rows=[v for v in runs if v['app']==app]
        print(app,[v['launch_ms'] for v in rows],[v['frame_timeline']['p95_ms'] for v in rows],[v['frame_timeline']['frames_after_swipe'] for v in rows], [v['focus'] for v in rows])
    print('EVENTS',len(events),'crashes',[l for l in events if re.search(r'am_(anr|crash)',l)])

(work/'analysis.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
