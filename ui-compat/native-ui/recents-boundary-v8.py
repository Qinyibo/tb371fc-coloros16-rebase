"""Bounded recents boundary reproduction; functional geometry, not a performance test."""
import json,re,shlex,subprocess,time
from pathlib import Path
root=Path.cwd();w=root/'ui-compat/native-ui/recents-boundary-v8';w.mkdir(exist_ok=False)
adb=['D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe','-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL']
def shell(cmd):
 r=subprocess.run(adb+['shell',cmd],capture_output=True,timeout=20);assert r.returncode==0,(cmd,r.stderr);return r.stdout.decode(errors='replace')
original=shell('wm user-rotation').strip();assert original in ['free','lock 0','lock 1','lock 2','lock 3']
start=shell('cat /proc/sys/kernel/random/boot_id; pidof system_server; pidof com.android.launcher');(w/'before.txt').write_text(start,encoding='utf-8')
records=[]
def capture(label,image=False):
 s=shell('dumpsys activity com.android.launcher/.Launcher');(w/(label+'.txt')).write_text(s,encoding='utf-8')
 lines=[x.strip() for x in s.splitlines() if 'app:id/overview_panel' in x or 'Current state:' in x]
 records.append({'label':label,'overview':lines,'task_view_instances':s.count('com.android.quickstep.views.OplusStackTaskView{')})
 if image:
  r=subprocess.run(adb+['exec-out','screencap -p'],check=True,capture_output=True,timeout=15);assert r.stdout[:4]==b'\x89PNG';(w/(label+'.png')).write_bytes(r.stdout)
try:
 shell('input keyevent KEYCODE_WAKEUP; wm dismiss-keyguard; wm user-rotation lock 0; input keyevent KEYCODE_HOME')
 for pkg in ['com.luna.music','com.ss.android.ugc.aweme']:
  component=shell('cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -p '+pkg).strip().splitlines()[-1]
  assert component.startswith(pkg+'/');shell('am start -W --windowingMode 1 -n '+component);time.sleep(.7)
 shell('/debug_ramdisk/su -c '+shlex.quote('CLASSPATH=/data/local/tmp/tb371fc-gesture-probe.jar app_process /system/bin GestureProbe 920 2920 920 1750 300 500'));time.sleep(1)
 capture('start',True)
 assert any('Current state: Overview' in x for x in records[-1]['overview'])
 for i in range(8):
  shell('input swipe 1660 1450 180 1450 400');time.sleep(.8);capture('left-'+str(i+1),i in [0,5,6,7])
 for i in range(3):
  shell('input swipe 180 1450 1660 1450 400');time.sleep(.8);capture('right-'+str(i+1),i==2)
finally:
 shell('wm user-rotation '+original+'; input keyevent KEYCODE_HOME; input keyevent KEYCODE_SLEEP')
(w/'summary.json').write_text(json.dumps({'scope':'Functional bounded sweep, no performance claim','records':records,'after':shell('cat /proc/sys/kernel/random/boot_id; pidof system_server; pidof com.android.launcher')},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for r in records:print(r['label'],r['overview'],r['task_view_instances'],flush=True)
