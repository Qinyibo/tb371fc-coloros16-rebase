"""Capture a bounded, read-only scheduler checkpoint."""
import argparse
import json
from pathlib import Path
import re
import shlex
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
ADB = ["D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe", "-P", "5037", "-s", "REPLACE_WITH_DEVICE_SERIAL"]


def shell(command):
    run = subprocess.run(ADB + ["shell", command], capture_output=True, timeout=20, check=True)
    return run.stdout.decode("utf-8", "replace").replace("\r", "")


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", required=True, type=Path)
parser.add_argument("--after-reboot", action="store_true")
args = parser.parse_args()
output = (ROOT / args.output).resolve()
assert output.is_relative_to(ROOT)
output.mkdir(parents=True, exist_ok=True)
if args.after_reboot:
    subprocess.run(ADB + ["wait-for-device"], timeout=50, check=True)
    for attempt in range(5):
        if shell("getprop sys.boot_completed").strip() == "1":
            break
        if attempt < 4:
            time.sleep(4)
    else:
        raise RuntimeError("Boot completion not observed")
command = """echo boot=$(cat /proc/sys/kernel/random/boot_id)
echo completed=$(getprop sys.boot_completed)
echo server=$(pidof system_server)
echo launcher=$(pidof com.android.launcher)
echo systemui=$(pidof com.android.systemui)
echo scheduler=$(getprop init.svc.tb371fc-scheduler)
pid=$(getprop init.svc_debug_pid.tb371fc-scheduler)
echo scheduler_pid=$pid
echo enforcing=$(getenforce)
if [ -n "$pid" ] && [ -r /proc/$pid/status ]; then
  echo domain=$(cat /proc/$pid/attr/current)
  grep '^Groups:' /proc/$pid/status
fi
echo boost=$(cat /dev/tb371fc-schedtune/foreground/schedtune.boost)
echo idle=$(cat /dev/tb371fc-schedtune/foreground/schedtune.prefer_idle)
echo tasks=$(cat /dev/tb371fc-schedtune/foreground/tasks)
echo mount=$(grep tb371fc-schedtune /proc/1/mountinfo)
echo modules=$(ls -A /data/adb/modules)
for p in $(pidof com.android.launcher com.android.systemui); do
  echo task_$p=$(grep ':schedtune:' /proc/$p/cgroup)
done
wm density
wm size
dumpsys power | grep -E 'mWakefulness=|mHalInteractiveModeEnabled='
sha256sum /system_ext/bin/tb371fc-scheduler /system_ext/etc/init/tb371fc-scheduler.rc /system_ext/priv-app/OplusLauncher/OplusLauncher.apk
dmesg | grep -E 'tb371fc_sched|tb371fc-sched' | tail -30
"""
snapshot = shell("/debug_ramdisk/su -c " + shlex.quote(command))
(output / "snapshot.txt").write_text(snapshot, encoding="utf-8")
fields = dict(re.findall(r"^([a-z][a-z0-9_]*)=(.*)$", snapshot, re.M))
core_pids = [fields.get("launcher"), fields.get("systemui")]
core_admission = {pid: fields.get(f"task_{pid}", "").endswith(":schedtune:/foreground") for pid in core_pids if pid}
summary = {
    "boot_id": fields.get("boot"),
    "boot_complete": fields.get("completed") == "1",
    "scheduler_pid": fields.get("scheduler_pid"),
    "scheduler_native_domain": fields.get("domain") == "u:r:tb371fc_scheduler:s0",
    "selinux_enforcing": fields.get("enforcing") == "Enforcing",
    "magisk_modules_empty": fields.get("modules") == "",
    "core_ui_foreground_membership": core_admission,
    "active_boost_observed": bool(fields.get("tasks")) and fields.get("boost") == "30" and fields.get("idle") == "1",
    "empty_neutral_group_observed": fields.get("boost") == "0" and fields.get("idle") == "0" and fields.get("tasks") == "",
    "wakefulness": next((line.split("=", 1)[1] for line in snapshot.splitlines() if "mWakefulness=" in line), None),
    "physical_380_dpi": "Physical density: 380" in snapshot,
}
(output / "result.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary))
