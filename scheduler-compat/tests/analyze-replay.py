"""Compare only the timed third-party workload window in each recorded phase."""
import argparse
import csv
from decimal import Decimal
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--work", type=Path, required=True)
args = parser.parse_args()
work = (ROOT / args.work).resolve()
assert work.is_relative_to(ROOT)
apps = "'com.android.launcher','com.android.systemui','com.ss.android.ugc.aweme','com.luna.music'"
for phase in ("A1-on", "B-off", "A2-on"):
    log = (work / (phase + "-workload.txt")).read_text(encoding="utf-8")
    stamps = re.findall(r"^(\d+\.\d+) \d+\.\d+$", log, re.M)
    for app in ("com.ss.android.ugc.aweme", "com.luna.music"):
        launches = re.findall(r"^Starting: Intent .* cmp=" + re.escape(app) + r"/", log, re.M)
        if len(launches) != 4:
            raise RuntimeError(f"{phase}: expected four starts of {app}, observed {len(launches)}")
    if len(stamps) != 2 or log.count("Starting: Intent") != 8:
        raise RuntimeError(f"{phase}: incomplete or unexpected workload")
    start, end = (int(Decimal(value) * 10**9) for value in stamps)
    where = f"ts BETWEEN {start} AND {end}"
    trace = work / phase / "heavy.pftrace"
    sql = f"""
WITH coverage AS (
    SELECT p.name, COUNT(DISTINCT f.surface_frame_token) AS frames
    FROM actual_frame_timeline_slice f JOIN process p USING(upid)
    WHERE f.{where} AND f.dur>=0 AND f.surface_frame_token>0
      AND p.name IN ('com.ss.android.ugc.aweme','com.luna.music')
    GROUP BY p.name
)
SELECT {start} AS start_ns, {end} AS end_ns,
       {start}<{end} AND start_ts<={start} AND end_ts>={end} AS trace_covers_workload,
       (SELECT COUNT(*) FROM coverage WHERE frames>0) AS third_party_apps_with_frames
FROM trace_bounds;
SELECT p.name AS process, COUNT(*) AS surface_frames,
       SUM(f.jank_type GLOB '*App Deadline Missed*') AS app_deadline_missed,
       ROUND(PERCENTILE(f.dur,95)/1e6,2) AS p95_ms,
       ROUND(MAX(f.dur)/1e6,2) AS max_ms
FROM actual_frame_timeline_slice f JOIN process p USING(upid)
WHERE f.{where} AND f.dur>=0 AND p.name IN ({apps}) GROUP BY p.name;
SELECT p.name AS process, t.name AS thread, COUNT(*) AS runnable_intervals,
       ROUND(PERCENTILE(s.dur,95)/1e6,2) AS p95_ms, ROUND(MAX(s.dur)/1e6,2) AS max_ms
FROM thread_state s JOIN thread t USING(utid) JOIN process p USING(upid)
WHERE s.{where} AND s.dur>=0 AND s.state IN ('R','R+')
AND p.name IN ({apps}) AND (t.is_main_thread OR t.name='RenderThread')
GROUP BY p.name,t.name;
SELECT CASE WHEN name GLOB '*:com.ss.android.ugc.aweme' THEN 'Douyin'
            WHEN name GLOB '*:com.luna.music' THEN 'Qishui'
            WHEN name GLOB '*:com.android.launcher' THEN 'Launcher'
            WHEN name GLOB '*:failed' THEN 'failed' ELSE 'other' END AS completion, COUNT(*) AS n
FROM slice WHERE {where} AND (name GLOB 'launchingActivity#*:completed-*' OR name GLOB 'launchingActivity#*:failed')
GROUP BY completion;
SELECT name,value FROM stats WHERE value>0 AND (name GLOB '*lost*' OR name GLOB '*overrun*' OR name GLOB '*overwrite*');
"""
    query = work / phase / "timed-workload.sql"
    query.write_text(sql, encoding="utf-8")
    result = subprocess.run(
        [str(ROOT / "tools/trace_processor_shell.exe"), "query", "--format", "csv", "-f", str(query), str(trace)],
        capture_output=True, check=True, timeout=40,
    )
    tables = result.stdout.decode("utf-8").replace("\r\n", "\n").strip().split("\n\n")
    coverage = next(csv.DictReader(tables[0].splitlines()))
    if coverage["trace_covers_workload"] != "1" or coverage["third_party_apps_with_frames"] != "2":
        raise RuntimeError(f"{phase}: trace lacks complete third-party frame coverage")
    (work / phase / "timed-workload.txt").write_bytes(result.stdout)
    print(phase, result.stdout.decode("utf-8"), flush=True)
