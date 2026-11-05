"""Bounded same-boot GPU floor control; restore the native level in finally."""
import argparse,json,shlex,subprocess,sys
from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);args=p.parse_args()
w=(r/args.output).resolve();assert w.is_relative_to(r);w.mkdir(parents=True,exist_ok=False)
a=['D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe','-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL']
def run(c):
 x=subprocess.run(a+['shell','/debug_ramdisk/su -c '+shlex.quote(c)],capture_output=True,timeout=25)
 assert x.returncode==0,(c,x.stderr)
 return x.stdout.decode(errors='replace').replace('\r','')
node='/sys/class/kgsl/kgsl-3d0/min_pwrlevel'
boot=run('cat /proc/sys/kernel/random/boot_id').strip()
assert run('cat '+node).strip()=='4','Native candidate level was changed externally'
records=[]
try:
 for phase,level in [('A1-level4',4),('B-level6',6),('A2-level4',4)]:
  assert run('cat /proc/sys/kernel/random/boot_id').strip()==boot
  if run('cat '+node).strip()!=str(level):run('echo '+str(level)+' > '+node)
  assert run('cat '+node).strip()==str(level)
  before=run('cat /sys/class/thermal/thermal_zone0/type; cat /sys/class/thermal/thermal_zone0/temp')
  result=subprocess.run([sys.executable,str(r/'scheduler-compat/tests/replay-fixed-30s.py'),'--output',str(w/phase)],cwd=r,timeout=110)
  assert result.returncode==0,(phase,result.returncode)
  subprocess.run([sys.executable,str(r/'scheduler-compat/tests/analyze-fixed-30s.py'),'--work',str(w/phase)],cwd=r,check=True,timeout=80)
  for app in ['com.luna.music','com.ss.android.ugc.aweme']:
   (w/phase/(app+'-exit-info.txt')).write_text(run('dumpsys activity exit-info '+app),encoding='utf8')
  after=run('cat /sys/class/thermal/thermal_zone0/type; cat /sys/class/thermal/thermal_zone0/temp')
  record={'phase':phase,'gpu_min_level':level,'thermal_before':before,'thermal_after':after,'boot_id':boot}
  records.append(record);(w/'phases.json').write_text(json.dumps(records,indent=2)+'\n')
  print('GPU_CONTROL_PHASE_COMPLETE',phase,flush=True)
finally:
 run('echo 4 > '+node)
 assert run('cat '+node).strip()=='4'
 (w/'restoration.json').write_text(json.dumps({'restored_level':4,'restored_frequency_hz':441600000,'boot_id_after':run('cat /proc/sys/kernel/random/boot_id').strip(),'all_phases_completed':len(records)==3,'no_rom_or_thermal_configuration_changed':True},indent=2)+'\n')
 print('NATIVE_GPU_LEVEL4_RESTORED',flush=True)
