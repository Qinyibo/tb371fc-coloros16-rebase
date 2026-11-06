from pathlib import Path
import subprocess,json
w=Path('ui-compat/native-ui/recents-boundary-v9');a=[r'D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe','-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL']
def run(cmd,t=20):
 p=subprocess.run(a+['exec-out',cmd],capture_output=True,timeout=t);assert p.returncode==0,p.stderr.decode(errors='replace');return p.stdout
run('input keyevent 224; wm dismiss-keyguard; wm user-rotation lock 0')
try:
 for pkg in ['com.ss.android.ugc.aweme','com.tencent.mobileqq']:
  c=run('cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.LAUNCHER '+pkg).decode().strip().splitlines()[-1]
  assert '/' in c,c
  run('am start -n '+c+'; sleep 2; input keyevent 3')
 run('input keyevent 187; sleep 0.8')
 for i in range(9):
  if i:run('input swipe 480 1450 1510 1450 260; sleep 0.35')
  if i in [0,4,8]:
   (w/f'multi-right-{i}.png').write_bytes(run('screencap -p'))
   (w/f'multi-right-{i}.zip').write_bytes(run('cmd window dump-visible-window-views'))
finally:run('wm user-rotation free')
print('BOUNDED_MULTI_TASK_EDGE_CAPTURED')
