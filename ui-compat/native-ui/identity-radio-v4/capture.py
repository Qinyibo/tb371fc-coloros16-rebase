"""Native identity and retained-page functional checks, without performance claims."""
import json,shlex,subprocess,time,xml.etree.ElementTree as ET
from pathlib import Path
r=Path.cwd();w=r/'ui-compat/native-ui/identity-radio-v4';out=w/'runtime';out.mkdir(exist_ok=False)
a=['D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe','-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL']
def shell(c,root=False):
 x=subprocess.run(a+['shell',('/debug_ramdisk/su -c '+shlex.quote(c)) if root else c],capture_output=True,timeout=25);assert x.returncode==0,(c,x.stdout[-500:],x.stderr);return x.stdout.decode(errors='replace').replace('\r','')
def snap(name):
 x=subprocess.run(a+['exec-out','screencap -p'],check=True,capture_output=True,timeout=15);assert x.stdout[:4]==b'\x89PNG';(out/(name+'.png')).write_bytes(x.stdout)
 shell('uiautomator dump /data/local/tmp/tb371fc-identity-v4.xml');s=shell('cat /data/local/tmp/tb371fc-identity-v4.xml');(out/(name+'.xml')).write_text(s,encoding='utf-8');return s
subprocess.run(a+['wait-for-device'],check=True,timeout=90)
for i in range(12):
 if shell('getprop sys.boot_completed').strip()=='1':break
 time.sleep(5)
else:raise RuntimeError('Boot completion timeout')
boot=shell('cat /proc/sys/kernel/random/boot_id; getprop sys.boot_completed; pidof system_server; pidof com.android.launcher; getenforce; pidof com.android.phone; cat /proc/uptime')
(out/'boot.txt').write_text(boot,encoding='utf-8');print(boot,flush=True)
assert boot.splitlines()[1]=='1' and boot.splitlines()[4]=='Enforcing'
phone=boot.splitlines()[5];assert phone.isdecimal()
identity={}
for key,expected in [('ro.product.model','TB371FC'),('ro.product.cpuinfo','SM8250_AC'),('ro.soc.model','SM8250-AC'),('ro.vendor.oplus.market.name','小新Pad Pro 12.7')]:
 value=shell('getprop '+key).strip();identity[key]=value;assert value==expected,(key,value)
for ns,key in [('global','device_name'),('global','revise_device_name'),('secure','bluetooth_name')]:
 value=shell('settings get '+ns+' '+key).strip();identity[ns+'/'+key]=value;assert value=='小新Pad Pro 12.7'
identity['cpu7_max_khz']=shell('cat /sys/devices/system/cpu/cpu7/cpufreq/cpuinfo_max_freq').strip();assert identity['cpu7_max_khz']=='3187200'
identity['bluetooth_service']=shell('dumpsys bluetooth_manager | grep -E "name:|mName|address:|state:"',True)
(out/'identity.json').write_text(json.dumps(identity,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert json.loads((w/'radio-build.json').read_bytes())['output_sha256'] in shell('sha256sum /system_ext/framework/oplus-telephony-common.jar',True)
original=shell('wm user-rotation').strip();assert original=='free';stamp=shell("date '+%m-%d %H:%M:%S.000'").strip()
try:
 shell('input keyevent KEYCODE_WAKEUP; wm dismiss-keyguard; input keyevent KEYCODE_HOME; wm user-rotation lock 1')
 shell('am start -W -a android.settings.DEVICE_INFO_SETTINGS',True);time.sleep(2);view=snap('about-landscape')
 if 'text="USB 用于"' in view:
  shell('input keyevent KEYCODE_BACK');view=snap('about-landscape-unblocked')
 print('ABOUT_TEXT',[(n.get('text'),n.get('bounds')) for n in ET.fromstring(view).iter('node') if n.get('text')][:35],flush=True)
 shell('input keyevent KEYCODE_HOME; am start -W -n com.android.phone/com.android.simsettings.activity.OplusSimSettingsActivity',True);time.sleep(4)
 view=snap('mobile-landscape');(out/'mobile-landscape-activity.txt').write_text(shell('dumpsys activity top'),encoding='utf-8')
 print('MOBILE_TEXT',[(n.get('text'),n.get('bounds')) for n in ET.fromstring(view).iter('node') if n.get('text')][:25],flush=True)
 shell('wm user-rotation lock 0');time.sleep(2);snap('mobile-portrait')
 shell('input keyevent KEYCODE_HOME; am start -W -a com.oplus.ota.MAIN',True);time.sleep(2);snap('ota-portrait')
finally:shell('wm user-rotation '+original+'; input keyevent KEYCODE_HOME; input keyevent KEYCODE_SLEEP')
(out/'after.txt').write_text(shell('cat /proc/sys/kernel/random/boot_id; pidof system_server; pidof com.android.launcher; pidof com.android.phone; cat /proc/uptime'),encoding='utf-8')
(out/'crash.txt').write_text(shell("logcat -b crash -d -T '"+stamp+"'"),encoding='utf-8')
(out/'runtime-log.txt').write_text(shell("logcat -d -T '"+stamp+"'"),encoding='utf-8')
assert phone==shell('pidof com.android.phone').strip(),'Phone process restarted'
print('NATIVE_TB_IDENTITY_AND_RETAINED_PAGES_CAPTURED_PHONE_PID_UNCHANGED',flush=True)
