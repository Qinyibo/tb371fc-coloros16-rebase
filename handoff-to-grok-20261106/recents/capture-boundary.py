from pathlib import Path
import subprocess,time,json
w=Path('ui-compat/native-ui/recents-boundary-v9');a=[r'D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe','-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL']
def run(cmd,t=15):
 p=subprocess.run(a+['exec-out',cmd],capture_output=True,timeout=t);assert p.returncode==0,(cmd,p.stderr.decode(errors='replace'));return p.stdout
run('input keyevent 224; wm dismiss-keyguard; input keyevent 187; sleep 0.6')
# Reopen overview from home to use a known state.
run('input keyevent 3; input keyevent 187; sleep 0.7')
try:
 for i in range(7):
  if i:run('input swipe 480 1450 1510 1450 260; sleep 0.35')
  (w/f'portrait-right-{i}.png').write_bytes(run('screencap -p'))
  if i in (0,3,6):(w/f'portrait-right-{i}.zip').write_bytes(run('cmd window dump-visible-window-views'))
 (w/'recents-log.txt').write_bytes(run('logcat -d -v threadtime -s StackPagedViewEx StackRecentsViewDelegate OplusRecentsViewImpl'))
finally:run('wm user-rotation free')
print('BOUNDED_6_RIGHT_SWIPES_CAPTURED; original rotation mode restored')
