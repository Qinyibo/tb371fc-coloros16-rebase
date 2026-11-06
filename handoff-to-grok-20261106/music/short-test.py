import subprocess,shlex,time,json,datetime
from pathlib import Path
out=Path('scheduler-compat/resume-20261106/heap-expand-toggle');a=r'D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe'
def root(cmd):
 p=subprocess.run([a,'-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL','exec-out','/debug_ramdisk/su -c '+shlex.quote(cmd)],capture_output=True,timeout=20)
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace'))
 return p.stdout
start=time.time();b=root('am start -W -n com.luna.music/com.luna.biz.main.main.MainActivity');(out/'controlled-start.txt').write_bytes(b)
print('Music launched; bounded 35-second normal foreground window.',flush=True)
time.sleep(35)
b=root('date; pidof com.luna.music; p=$(pidof com.luna.music); if [ -n "$p" ]; then cat /proc/$p/status | head -6; grep -E "dalvik.*(region space|bitmap)|expand" /proc/$p/maps; fi; grep enableArtHeapExpandV4 /data/user/0/com.luna.music/shared_prefs/luna_launch_local_shared_preferences.xml; dumpsys activity exit-info com.luna.music')
(out/'controlled-after-35s.txt').write_bytes(b)
print(b.decode(errors='replace')[:2400],flush=True)
(out/'controlled-window.json').write_text(json.dumps({'start_epoch':start,'end_epoch':time.time(),'method':'normal foreground launch, 35s; no GC pressure or memory injection'},indent=2)+'\n')
