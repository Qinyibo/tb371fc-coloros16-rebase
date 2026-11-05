"""Temporary private-ABI diagnostic; restore the real identity in finally."""
from pathlib import Path
import argparse,json,shlex,subprocess,sys,time
r=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--test-manufacturer',choices=['OnePlus','LENOVO'],default='OnePlus');p.add_argument('--output',type=Path,default=Path('scheduler-compat/gpu-floor-native-v7/music-manufacturer-control'));args=p.parse_args()
w=(r/args.output).resolve();assert w.is_relative_to(r)
w.mkdir(parents=True,exist_ok=False)
a=['D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe','-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL']
def run(c):
 x=subprocess.run(a+['shell','/debug_ramdisk/su -c '+shlex.quote(c)],capture_output=True,timeout=25)
 assert x.returncode==0,(c,x.stderr)
 return x.stdout.decode(errors='replace').replace('\r','')
original=run('getprop ro.product.manufacturer').strip()
brand=run('getprop ro.product.brand').strip()
boot=run('cat /proc/sys/kernel/random/boot_id').strip()
assert original=='LENOVO' and brand=='Lenovo'
(w/'before.json').write_text(json.dumps({'manufacturer':original,'brand':brand,'boot_id':boot,'purpose':'Diagnostic only; no candidate identity change; application data retained'},indent=2)+'\n')
try:
 if args.test_manufacturer!=original:run('/debug_ramdisk/resetprop -n ro.product.manufacturer '+args.test_manufacturer)
 assert run('getprop ro.product.manufacturer').strip()==args.test_manufacturer
 run('am force-stop com.luna.music')
 subprocess.run([sys.executable,str(r/'scheduler-compat/tests/replay-fixed-30s.py'),'--output',str(w/'replay')],cwd=r,check=True,timeout=110)
 (w/'exit-info.txt').write_text(run('dumpsys activity exit-info com.luna.music'),encoding='utf8')
 (w/'music-maps.txt').write_text(run('p=$(pidof com.luna.music); echo PID=$p; if [ -n "$p" ]; then cat /proc/$p/maps; fi'),encoding='utf8')
 log=run('logcat -b main -b system -d -v epoch -t 15000')
 (w/'heap-log.txt').write_text('\n'.join(l for l in log.splitlines() if any(k in l.lower() for k in ['heap_expand','heapexpand','heap expand','manufacturer:','brand:','heap finish','heapgcoptimizer']))+'\n',encoding='utf8')
finally:
 run('/debug_ramdisk/resetprop -n ro.product.manufacturer '+shlex.quote(original))
 assert run('getprop ro.product.manufacturer').strip()==original
 assert run('getprop ro.product.brand').strip()==brand
 run('am force-stop com.luna.music')
 after={'manufacturer':run('getprop ro.product.manufacturer').strip(),'brand':run('getprop ro.product.brand').strip(),'boot_id':run('cat /proc/sys/kernel/random/boot_id').strip(),'gpu_min_level':run('cat /sys/class/kgsl/kgsl-3d0/min_pwrlevel').strip(),'application_data_cleared':False,'test_app_stopped_after_diagnostic':True}
 (w/'restored.json').write_text(json.dumps(after,indent=2)+'\n')
 print('REAL_IDENTITY_RESTORED',json.dumps(after),flush=True)
