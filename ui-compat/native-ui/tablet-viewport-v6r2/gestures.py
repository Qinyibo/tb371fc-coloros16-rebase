"""Bounded input-dispatcher gesture smoke tests; this does not test physical touch IRQs."""
import argparse
from pathlib import Path
import re
import subprocess
import time

root=Path(__file__).resolve().parents[3]
parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=['2','4'],required=True);parser.add_argument('--rotation',choices=['0','1'],default='0');parser.add_argument('--output',required=True);args=parser.parse_args()
work=(root/args.output).resolve();assert work.is_relative_to(root);work.mkdir(parents=True,exist_ok=True)
adb=['D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe','-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL']
commands=[]

def shell(command):
    proc=subprocess.run(adb+['shell',command],capture_output=True,timeout=25)
    message=(proc.stdout+proc.stderr).decode(errors='replace').replace('\r','')
    commands.append(command+'\n'+message)
    (work/'commands.txt').write_text('\n'.join(commands),encoding='utf-8')
    assert proc.returncode==0,(command,message[-600:])
    return message

(work/'boot-status.txt').write_text(shell('cat /proc/sys/kernel/random/boot_id; pidof system_server; pidof com.android.launcher; getprop sys.boot_completed; getprop persist.sys.oplus.anim_level'),encoding='utf-8')
assert shell('getprop sys.boot_completed').strip()=='1'
assert shell('getprop persist.sys.oplus.anim_level').strip()==args.mode
original=shell('wm user-rotation').strip();assert original=='free' or re.fullmatch(r'lock [0-3]',original)
subprocess.run(adb+['push',str(root/'ui-compat/native-ui/gesture-probe.jar'),'/data/local/tmp/tb371fc-gesture-probe.jar'],check=True,timeout=20)
try:
    shell('input keyevent KEYCODE_WAKEUP; wm dismiss-keyguard; wm user-rotation lock '+args.rotation+'; input keyevent KEYCODE_HOME')
    time.sleep(2);shell('input keyevent KEYCODE_BACK');time.sleep(.5)
    shell('am start -W -a android.intent.action.MAIN -c android.intent.category.HOME');time.sleep(1)
    for name,package in [('desktop',None),('app','com.ss.android.ugc.aweme')]:
        if package:
            component=shell('cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -p '+package).strip().splitlines()[-1]
            assert component.startswith(package+'/');shell('am start -W --windowingMode 1 -n '+component);time.sleep(1)
        focus=shell('dumpsys window | grep mCurrentFocus')
        assert (package if package else 'com.android.launcher') in focus,(name,focus)
        rotation = 'ROTATION_'+('0' if args.rotation=='0' else '90')
        assert rotation in shell('dumpsys window displays | grep -m1 mDisplayRotation'), (name, rotation)
        points = '920 2920 920 1750' if args.rotation=='0' else '1472 1816 1472 1094'
        shell('/debug_ramdisk/su -c "CLASSPATH=/data/local/tmp/tb371fc-gesture-probe.jar app_process /system/bin GestureProbe '+points+' 300 500"')
        time.sleep(2)
        data=shell('dumpsys activity com.android.launcher/.Launcher');(work/(name+'-launcher.txt')).write_text(data,encoding='utf-8')
        proc=subprocess.run(adb+['exec-out','screencap -p'],capture_output=True,timeout=15);assert proc.returncode==0 and proc.stdout.startswith(b'\x89PNG')
        (work/(name+'.png')).write_bytes(proc.stdout)
        shell('input keyevent KEYCODE_HOME');time.sleep(.7)
finally:
    shell('wm user-rotation '+original+'; input keyevent KEYCODE_HOME; input keyevent KEYCODE_SLEEP')
print('HELD_GESTURE_CAPTURES_READY_FOR_REVIEW',args.mode,flush=True)
