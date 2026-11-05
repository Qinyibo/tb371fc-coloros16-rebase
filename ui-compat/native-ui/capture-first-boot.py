from pathlib import Path
import argparse
import subprocess
import time

root = Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--output',default='ui-compat/native-ui/candidate/runtime')
args=parser.parse_args()
work = (root / args.output).resolve()
assert work.is_relative_to(root)
work.mkdir(exist_ok=True)
adb = ['D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe', '-P', '5037', '-s', 'REPLACE_WITH_DEVICE_SERIAL']


def run(command, name=None, binary=False):
    args = ['exec-out', command] if binary else ['shell', command]
    proc = subprocess.run(adb + args, capture_output=True, timeout=25)
    if name:
        (work / name).write_bytes(proc.stdout)
        if proc.stderr:
            (work / (name + '.stderr')).write_bytes(proc.stderr)
    assert proc.returncode == 0, (command, proc.stderr[-500:])
    return proc.stdout if binary else proc.stdout.decode(errors='replace').replace('\r', '')


# A single delayed snapshot, not device polling. First boot may compile new DEX.
time.sleep(25)
status = run('getprop sys.boot_completed; cat /proc/sys/kernel/random/boot_id; cat /proc/uptime; '
             'pidof system_server; pidof com.android.launcher; getprop persist.sys.oplus.anim_level; '
             'getprop init.svc.tb371fc-speaker; getenforce', 'boot-status.txt')
print(status, flush=True)
if status.splitlines()[0] != '1':
    print('BOOT_NOT_COMPLETE_IN_SINGLE_SNAPSHOT', flush=True)
    raise SystemExit(0)
run('logcat -b crash -d', 'crash.txt')
run('/debug_ramdisk/su -c "abx2xml /data/system/display-manager-state.xml -"', 'display-store.xml')
run('dumpsys display', 'display.txt')
original_rotation = run('wm user-rotation').strip()
assert original_rotation == 'free', original_rotation
run('input keyevent KEYCODE_WAKEUP; wm dismiss-keyguard; input keyevent KEYCODE_BACK')
time.sleep(.5)
try:
    for rotation, label in ((0, 'portrait'), (1, 'landscape')):
        run(f'input keyevent KEYCODE_WAKEUP; wm dismiss-keyguard; wm user-rotation lock {rotation}; input keyevent KEYCODE_HOME')
        time.sleep(3)
        run('dumpsys activity com.android.launcher/.Launcher', label + '-launcher.txt')
        image = run('screencap -p', label + '.png', binary=True)
        assert image.startswith(b'\x89PNG\r\n\x1a\n')
    run('am start -a android.settings.DISPLAY_SETTINGS', 'settings-start.txt')
    time.sleep(3)
    run('uiautomator dump /data/local/tmp/tb371fc-native-ui-settings.xml')
    run('cat /data/local/tmp/tb371fc-native-ui-settings.xml', 'settings-ui.xml')
    run('screencap -p', 'settings.png', binary=True)
finally:
    run('wm user-rotation free')
run('logcat -b crash -d', 'crash-after-ui.txt')
run('logcat -d -s TB371FCAnimation:E TB371FCAnimation:I', 'settings-helper-log.txt')
print('NATIVE_UI_FIRST_BOOT_AND_ORIENTATION_CAPTURE_COMPLETE', flush=True)
