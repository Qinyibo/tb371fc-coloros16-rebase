"""User-authorized fixed third-party load; preserve GPU and scheduler policy."""
import argparse,json,re,shlex,subprocess,sys,time
from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);args=p.parse_args()
w=(r/args.output).resolve();assert w.is_relative_to(r);w.mkdir(exist_ok=False,parents=True)
a=['D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe','-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL']
apps=['com.ss.android.ugc.aweme','com.luna.music']
def run(c,root=False,timeout=25):
 x=subprocess.run(a+['shell',('/debug_ramdisk/su -c '+shlex.quote(c)) if root else c],capture_output=True,timeout=timeout)
 assert x.returncode==0,(c,x.stdout[-500:],x.stderr)
 return x.stdout.decode(errors='replace').replace('\r','')
original_power=run('dumpsys power | grep mWakefulness=')
assert 'secure=false' in run('dumpsys window policy | grep -m1 secure=')
policy_command='cat /proc/sys/kernel/random/boot_id; getprop init.svc.tb371fc-scheduler; cat /sys/class/kgsl/kgsl-3d0/min_pwrlevel'
before=run(policy_command,True).strip();(w/'policy-before.txt').write_text(before,encoding='utf8')
third=set(run('pm list packages -3').splitlines());assert all('package:'+s in third for s in apps)
components={}
for app in apps:
 c=run('cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -p '+app).strip().splitlines()[-1]
 assert c.startswith(app+'/'),c;components[app]=c
def launch(app,wait=False):
 return 'am start '+('-W ' if wait else '')+'--windowingMode 1 -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -n '+shlex.quote(components[app])
capture=None
run('input keyevent KEYCODE_WAKEUP; wm dismiss-keyguard; input keyevent KEYCODE_HOME')
try:
 for app in apps:
  result=run(launch(app,True));time.sleep(3)
  focus=run('dumpsys window | grep -m1 mCurrentFocus');assert app in focus,focus
  (w/(app+'-warm.txt')).write_text(result+focus,encoding='utf8')
 display=run('dumpsys window displays | grep -m1 mDisplayRotation')
 m=re.search(r'mBounds=Rect\(0, 0 - (\d+), (\d+)\)',display);assert m,display
 width,height=map(int,m.groups());home=f'cmd input touchscreen swipe {width//2} {height-17} {width//2} {int(height*.57)} 160'
 commands=[]
 for _ in range(8):
  for app in apps:commands += [launch(app),'sleep 0.55',home,'sleep 0.25']
 text='; '.join(commands)
 (w/'workload.sh').write_text(text+'\n',encoding='utf8')
 capture=subprocess.Popen([sys.executable,str(r/'scheduler-compat/tests/capture-heavy.py'),'--duration','30','--workload-driver','automation','--output',str(w/'capture')],cwd=r)
 deadline=time.monotonic()+10
 while time.monotonic()<deadline:
  log=w/'capture/capture.log'
  if log.exists() and b'Connected to the Perfetto' in log.read_bytes():break
  assert capture.poll() is None,'Capture ended before workload'
  time.sleep(.1)
 else:raise RuntimeError('No confirmed capture start; input replay not started')
 start=run('cat /proc/uptime').strip()
 output=run(text,timeout=40)
 end=run('cat /proc/uptime').strip()
 (w/'workload.txt').write_text(start+'\n'+output+end+'\n',encoding='utf8')
 assert capture.wait(timeout=55)==0,'Capture did not complete'
 after=run(policy_command,True).strip();(w/'policy-after.txt').write_text(after,encoding='utf8')
 assert before==after,'Boot/scheduler/GPU policy changed during test'
 (w/'result.json').write_text(json.dumps({'apps':apps,'explicit_starts_per_app':8,'duration_seconds':30,'input_injected':True,'user_authorization':'你操作','data_cleared':False,'apps_force_stopped':False,'scheduler_and_gpu_policy_unchanged':True,'subjective_acceptance':False,'diagnostic_only':True},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print('FIXED_THIRD_PARTY_REPLAY_CAPTURED_POLICY_UNCHANGED',flush=True)
finally:
 if capture is not None and capture.poll() is None:
  capture.wait(timeout=55)
 run('input keyevent KEYCODE_HOME'+('; input keyevent KEYCODE_SLEEP' if 'mWakefulness=Asleep' in original_power else ''))
