from pathlib import Path
import subprocess
w=Path(__file__).resolve().parent;a=[r'D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe','-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL']
def run(cmd):
 p=subprocess.run(a+['exec-out',cmd],capture_output=True,timeout=18);assert p.returncode==0,p.stderr.decode(errors='replace');return p.stdout
run('input keyevent 224; wm dismiss-keyguard; input keyevent 3; input keyevent 187; sleep 0.6')
try:
 run('wm user-rotation lock 3; sleep 1; wm user-rotation lock 0; sleep 1')
 for i in range(13):
  if i:run('input swipe 480 1450 1510 1450 220; sleep 0.25')
  if i in [0,6,12]:
   run('sleep 1')
   (w/f'rotated-right-{i}.zip').write_bytes(run('cmd window dump-visible-window-views'))
   (w/f'rotated-right-{i}.png').write_bytes(run('screencap -p'))
finally:run('wm user-rotation free; input keyevent 3')
print('BOUNDED_ROTATION_EDGE_CAPTURED_ORIGINAL_ROTATION_RESTORED')
