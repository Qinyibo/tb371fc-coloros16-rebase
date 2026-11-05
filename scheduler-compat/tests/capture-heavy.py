"""Record one user-driven third-party load with no input injection."""
import argparse
import json
from pathlib import Path
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[2]
ADB = ["D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe", "-P", "5037", "-s", "REPLACE_WITH_DEVICE_SERIAL"]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--duration", type=int, choices=(12, 25, 30, 120), default=25)
parser.add_argument("--workload-driver", choices=("user", "automation"), default="user")
args = parser.parse_args()
output = (ROOT / args.output).resolve()
assert output.is_relative_to(ROOT)
output.mkdir(parents=True, exist_ok=False)
old = ROOT / "ui-compat/native-ui/user-feedback-20261105/compact-trace.pbtxt"
config = output / "config.pbtxt"
text = old.read_text(encoding="utf-8").replace("duration_ms: 15000", f"duration_ms: {args.duration * 1000}").replace("tb371fc-compact-repro-20261105", "tb371fc-heavy-v4")
# Keep the workload apps' own drawing slices alongside frame and scheduling data.
text = text.replace(' atrace_apps: "com.android.systemui"', ' atrace_apps: "com.android.systemui"\n atrace_apps: "com.ss.android.ugc.aweme"\n atrace_apps: "com.luna.music"')
# Record real process creation/renames so specialized USAPs retain app identity.
text = text.replace(' ftrace_events: "sched/sched_waking"', ' ftrace_events: "sched/sched_waking"\n ftrace_events: "task/task_newtask"\n ftrace_events: "task/task_rename"\n ftrace_events: "sched/sched_process_exit"')
text = text.replace('scan_all_processes_on_start: true', 'scan_all_processes_on_start: true proc_stats_poll_ms: 1000')
if args.duration == 120:
    text = text.replace('size_kb: 131072', 'size_kb: 262144')
config.write_text(text, encoding="utf-8")
remote_config = "/data/local/tmp/tb371fc-heavy-v4.pbtxt"
remote_trace = "/data/local/tmp/tb371fc-heavy-v4.pftrace"
subprocess.run(ADB + ["push", str(config), remote_config], check=True, timeout=15, capture_output=True)
snapshot = "cat /proc/uptime; cat /proc/sys/kernel/random/boot_id; date -u '+%s.%N'; cat /sys/class/kgsl/kgsl-3d0/min_pwrlevel"
before = subprocess.run(ADB + ["shell", "/debug_ramdisk/su -c " + shlex.quote(snapshot)], capture_output=True, check=True, timeout=15)
(output / "capture-start-state.txt").write_bytes(before.stdout)
with (output / "capture.log").open("wb") as log:
    subprocess.run(ADB + ["shell", f'/debug_ramdisk/su -c "perfetto --txt -c {remote_config} -o {remote_trace}"'], check=True, timeout=args.duration + 20, stdout=log, stderr=subprocess.STDOUT)
after = subprocess.run(ADB + ["shell", "/debug_ramdisk/su -c " + shlex.quote(snapshot)], capture_output=True, check=True, timeout=15)
(output / "capture-end-state.txt").write_bytes(after.stdout)
# Read the existing bounded event buffer once; never start/stop another collector.
with (output / "process-events.log").open("wb") as events:
    event_read = subprocess.run(ADB + ["exec-out", "/debug_ramdisk/su -c " + shlex.quote("logcat -b events -d -v epoch")], stdout=events, stderr=subprocess.PIPE, timeout=20)
(output / "event-read-stderr.txt").write_bytes(event_read.stderr)
(output / "capture-method.json").write_text(json.dumps({"process_lifecycle_ftrace": True, "process_metadata_poll_ms": 1000, "event_buffer_read_returncode": event_read.returncode, "event_buffer_full_interval_coverage_not_assumed": True, "input_injected": args.workload_driver == "automation", "workload_driver": args.workload_driver, "scheduler_or_gpu_changed_during_capture": False}, indent=2) + "\n", encoding="utf-8")
trace = output / "heavy.pftrace"
with trace.open("wb") as raw:
    pull = subprocess.run(ADB + ["exec-out", f'/debug_ramdisk/su -c "cat {remote_trace}"'], check=True, timeout=30, stdout=raw, stderr=subprocess.PIPE)
if trace.stat().st_size < 100_000:
    raise RuntimeError("Trace is too small to establish a workload")
print(f"Captured {trace.stat().st_size} bytes", flush=True)
