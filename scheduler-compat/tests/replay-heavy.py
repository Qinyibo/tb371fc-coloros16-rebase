"""Bounded third-party app stress and same-boot scheduler A/B/A capture."""
import argparse
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
ADB = ["D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe", "-P", "5037", "-s", "REPLACE_WITH_DEVICE_SERIAL"]
APPS = ("com.ss.android.ugc.aweme", "com.luna.music")
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--resume-after-a1", action="store_true")
args = parser.parse_args()
output = (ROOT / args.output).resolve()
assert output.is_relative_to(ROOT)
output.mkdir(parents=True, exist_ok=args.resume_after_a1)


def shell(command, *, root=False, timeout=18):
    if root:
        command = "/debug_ramdisk/su -c " + shlex.quote(command)
    run = subprocess.run(ADB + ["shell", command], capture_output=True, timeout=timeout, check=True)
    return run.stdout.decode("utf-8", "replace").replace("\r", "")


def scheduler_state():
    return shell("getprop init.svc.tb371fc-scheduler; cat /dev/tb371fc-schedtune/foreground/schedtune.boost; cat /dev/tb371fc-schedtune/foreground/tasks", root=True).splitlines()


def scheduler(enable):
    if enable:
        shell("setprop ctl.start tb371fc-scheduler", root=True)
    else:
        pid = shell("getprop init.svc_debug_pid.tb371fc-scheduler", root=True).strip()
        assert pid.isdecimal() and int(pid) > 1, pid
        shell(f'test "$(readlink /proc/{pid}/exe)" = /system_ext/bin/tb371fc-scheduler && kill -TERM {pid}', root=True)
    time.sleep(1.5)
    state = scheduler_state()
    assert state[:2] == (["running", "30"] if enable else ["stopped", "0"]), state
    assert (len(state) > 2) == enable, state


assert "mWakefulness=Asleep" in shell("dumpsys power | grep mWakefulness="), "Device is in use"
assert "secure=false" in shell("dumpsys window policy | grep -m1 secure="), "Keyguard needs the user"
assert shell("getprop init.svc.tb371fc-scheduler").strip() == "running"
third_party = set(shell("pm list packages -3").splitlines())
if not all(f"package:{app}" in third_party for app in APPS):
    raise RuntimeError("The replay requires both installed third-party apps")
boot = shell("cat /proc/sys/kernel/random/boot_id").strip()
if args.resume_after_a1:
    assert (output / "A1-on/heavy.pftrace").is_file() and (output / "A1-on-workload.txt").is_file()
    assert boot == json.loads((ROOT / "scheduler-compat/candidate-package-info/first-boot/result.json").read_text())["boot_id"]
components = {}
for app in APPS:
    out = shell("cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -p " + app).strip().splitlines()
    assert out and out[-1].startswith(app + "/"), out
    components[app] = out[-1]


def launch(app, wait=False):
    return "am start " + ("-W " if wait else "") + "--windowingMode 1 -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -n " + shlex.quote(components[app])


def focus():
    return shell("dumpsys window | grep -m1 mCurrentFocus")


shell("input keyevent KEYCODE_WAKEUP; wm dismiss-keyguard; input keyevent KEYCODE_HOME")
try:
    for app in APPS:
        result = shell(launch(app, wait=True))
        time.sleep(2)
        window = focus()
        (output / (app + "-warm.txt")).write_text(result + window, encoding="utf-8")
        assert app in window, window
    display = shell("dumpsys window displays | grep -m1 mDisplayRotation")
    match = re.search(r"mBounds=Rect\(0, 0 - (\d+), (\d+)\)", display)
    assert match, display[:160]
    width, height = map(int, match.groups())
    swipe = f"cmd input touchscreen swipe {width//2} {height-17} {width//2} {int(height*.57)} 160"
    workload = []
    for _ in range(4):
        for app in APPS:
            workload += [launch(app), "sleep 0.24", swipe, "sleep 0.16"]
    commands = "; ".join(workload)
    phases = [("A1-on", True), ("B-off", False), ("A2-on", True)]
    for phase, enabled in phases[1:] if args.resume_after_a1 else phases:
        if phase != "A1-on":
            scheduler(enabled)
        else:
            assert scheduler_state()[:2] == ["running", "30"]
        shell("input keyevent KEYCODE_HOME")
        time.sleep(.6)
        run = subprocess.Popen([sys.executable, str(ROOT / "scheduler-compat/tests/capture-heavy.py"), "--duration", "12", "--workload-driver", "automation", "--output", str(output / phase)], cwd=ROOT)
        try:
            time.sleep(2)
            before = shell("cat /proc/uptime").strip()
            log = shell(commands, timeout=22)
            after = shell("cat /proc/uptime").strip()
            (output / (phase + "-workload.txt")).write_text(before + "\n" + log + after + "\n" + focus(), encoding="utf-8")
        finally:
            if run.wait(timeout=65) != 0:
                raise RuntimeError(f"Capture failed for {phase}")
        print(f"{phase} workload captured", flush=True)
finally:
    # Return the same ROM service to its original enabled state.
    if shell("getprop init.svc.tb371fc-scheduler").strip() != "running":
        scheduler(True)
    shell("input keyevent KEYCODE_HOME; input keyevent KEYCODE_SLEEP")
