"""Check the native GPU boot policy without changing any driver parameter."""
from pathlib import Path
import hashlib,json,shlex,subprocess,time
w=Path(__file__).resolve().parent;out=w/'runtime';out.mkdir(exist_ok=False)
a=['D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe','-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL']
def run(c):
 x=subprocess.run(a+['shell','/debug_ramdisk/su -c '+shlex.quote(c)],capture_output=True,timeout=25)
 assert x.returncode==0,(c,x.stdout[-500:],x.stderr)
 return x.stdout.decode(errors='replace').replace('\r','')
subprocess.run(a+['wait-for-device'],check=True,timeout=90)
for i in range(12):
 if run('getprop sys.boot_completed').strip()=='1':break
 time.sleep(5)
else:raise RuntimeError('Boot completion not verified')
assert run('getenforce').strip()=='Enforcing'
assert run('getprop vendor.post_boot.parsed').strip()=='1'
assert run('getprop ro.product.board').strip()=='spinel'
assert '76995e3ce9469a605ed0f07c23d9e3c1f92582f026107202d4ff76941d810c07' in run('sha256sum /system_ext/bin/tb371fc-scheduler')
expected=hashlib.sha256((w/'tb371fc-gpu-profile.rc').read_bytes()).hexdigest()
assert expected in run('sha256sum /vendor/etc/init/tb371fc-gpu-profile.rc')
first=run('cat /sys/class/kgsl/kgsl-3d0/min_pwrlevel').strip()
(out/'initial-level.txt').write_text(first+'\n')
time.sleep(20)
later=run('cat /sys/class/kgsl/kgsl-3d0/min_pwrlevel').strip()
table=[int(s) for s in run('cat /sys/class/kgsl/kgsl-3d0/devfreq/available_frequencies').split()]
maximum=run('cat /sys/class/kgsl/kgsl-3d0/max_pwrlevel').strip()
clock=run('cat /sys/class/kgsl/kgsl-3d0/gpuclk').strip()
boot=run('cat /proc/sys/kernel/random/boot_id; pidof system_server; pidof com.android.launcher; pidof com.android.phone; cat /proc/uptime')
(out/'boot.txt').write_text(boot,encoding='utf8')
if first!='4' or later!='4':
 (out/'init-failure-log.txt').write_text(run("logcat -b all -d | grep -i -E 'tb371fc-gpu-profile|min_pwrlevel|avc: denied.*(vendor_init|kgsl)' ; true"),encoding='utf8')
result={'native_file_sha256':expected,'first_level':first,'level_after_20s':later,'frequency_table_hz':table,'minimum_frequency_hz':table[4] if len(table)>4 else None,'max_pwrlevel':maximum,'gpuclk_observed':clock,'selinux_enforcing':True,'previous_v5_controller_verified':True,'driver_parameter_written_by_this_verifier':False,'input_injected':False,'performance_verified':False,'long_term_power_thermal_verified':False}
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
assert first==later=='4' and table[4]==441600000,result
assert run('getprop ro.product.brand').strip()=='Lenovo'
assert run('getprop ro.product.cpuinfo').strip()=='SM8250_AC'
print(json.dumps(result),flush=True)
