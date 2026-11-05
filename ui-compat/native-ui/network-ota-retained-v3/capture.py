"""Verify retained mobile/OTA pages against real boot and native endpoint state."""
import hashlib,json,re,shlex,subprocess,time,xml.etree.ElementTree as ET
from pathlib import Path
r=Path.cwd();w=r/'ui-compat/native-ui/network-ota-retained-v3';out=w/'runtime';out.mkdir(exist_ok=True)
a=['D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe','-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL']
def shell(c,root=False):
 x=subprocess.run(a+['shell',('/debug_ramdisk/su -c '+shlex.quote(c)) if root else c],capture_output=True,timeout=25);assert x.returncode==0,(c,x.stdout[-500:],x.stderr);return x.stdout.decode(errors='replace').replace('\r','')
def snap(name):
 x=subprocess.run(a+['exec-out','screencap -p'],check=True,capture_output=True,timeout=15);assert x.stdout[:4]==b'\x89PNG';(out/(name+'.png')).write_bytes(x.stdout)
 shell('uiautomator dump /data/local/tmp/tb371fc-retained-v3.xml')
 s=shell('cat /data/local/tmp/tb371fc-retained-v3.xml');(out/(name+'.xml')).write_text(s,encoding='utf-8');return s
subprocess.run(a+['wait-for-device'],check=True,timeout=90)
for i in range(12):
 if shell('getprop sys.boot_completed').strip()=='1':break
 time.sleep(5)
else:raise RuntimeError('Boot completion did not arrive within bounded window')
boot=shell('cat /proc/sys/kernel/random/boot_id; getprop sys.boot_completed; pidof system_server; pidof com.android.launcher; getenforce; getprop ro.carrier; wm density; settings get system font_scale; pidof com.android.phone; cat /proc/uptime')
if (out/'boot.txt').exists():
 first=(out/'boot.txt').read_text().splitlines()
 assert [boot.splitlines()[i] for i in [0,2,3,8]]==[first[i] for i in [0,2,3,8]],'Boot or phone process changed before retry'
 (out/'capture-boot.txt').write_text(boot,encoding='utf-8')
else:(out/'boot.txt').write_text(boot,encoding='utf-8')
print(boot,flush=True)
assert 'Enforcing' in boot and 'Physical density: 370' in boot
assert '7455cb251c4ebf4c1685351e69ee3d150c8bb586e46916c17f6bb86c5e5ce737' in shell('sha256sum /system_ext/framework/oplus-telephony-common.jar',True)
assert '4fc2b16c991195d8bd6a0b760678ea9e074f9450287475453ff79bd64224479f' in shell('sha256sum /system_ext/app/OTA/OTA.apk')
original=shell('wm user-rotation').strip();assert original=='free'
stamp=shell("date '+%m-%d %H:%M:%S.000'").strip()
policy=json.loads((w/'endpoint-policy.json').read_bytes());query='content query --uri content://com.oplus.customize.coreapp.configmanager.configprovider.AppFeatureProvider/app_feature --where '+shlex.quote('featurename in ('+','.join("'"+key+"'" for key in policy['keys'])+')')
features=shell(query,True);(out/'active-update-endpoints.txt').write_text(features,encoding='utf-8')
assert features.count(policy['endpoint'])==len(policy['keys']),features
print('NATIVE_PROVIDER_ALL_UPDATE_DESTINATIONS_VERIFIED',flush=True)
# Restore the previous reversible package-enabled setting as well as the image payload.
(out/'ota-enabled.txt').write_text(shell('pm default-state --user 0 com.oplus.ota',True),encoding='utf-8')
try:
 shell('input keyevent KEYCODE_WAKEUP; wm dismiss-keyguard; input keyevent KEYCODE_HOME; wm user-rotation lock 1')
 shell('am start -W -n com.android.phone/com.android.simsettings.activity.OplusSimSettingsActivity',True);time.sleep(1)
 view=snap('mobile-standalone')
 if 'text="USB 用于"' in view:
  shell('input keyevent KEYCODE_BACK');view=snap('mobile-standalone-unblocked')
 (out/'mobile-activity.txt').write_text(shell('dumpsys activity top'),encoding='utf-8')
 print('MOBILE_PAGE_TEXT',[(n.get('text'),n.get('bounds')) for n in ET.fromstring(view).iter('node') if n.get('text')][:20],flush=True)
 shell('input keyevent KEYCODE_HOME; am start -W -a android.settings.SETTINGS');time.sleep(.7)
 snap('settings-restored')
 shell('input keyevent KEYCODE_HOME')
 component=shell('cmd package resolve-activity --brief -a com.oplus.ota.MAIN').strip().splitlines()[-1];assert component.startswith('com.oplus.ota/'),component
 (out/'ota-component.txt').write_text(component,encoding='utf-8')
 shell('am start -W -n '+component,True);time.sleep(2);view=snap('ota-restored')
 print('OTA_PAGE_TEXT',[(n.get('text'),n.get('bounds')) for n in ET.fromstring(view).iter('node') if n.get('text')][:25],flush=True)
 (out/'ota-activity.txt').write_text(shell('dumpsys activity top'),encoding='utf-8')
finally:shell('wm user-rotation '+original+'; input keyevent KEYCODE_HOME; input keyevent KEYCODE_SLEEP')
(out/'crash.txt').write_text(shell("logcat -b crash -d -T '"+stamp+"'"),encoding='utf-8')
(out/'runtime-log.txt').write_text(shell("logcat -d -T '"+stamp+"'"),encoding='utf-8')
(out/'after.txt').write_text(shell('cat /proc/sys/kernel/random/boot_id; pidof system_server; pidof com.android.launcher; pidof com.android.phone; cat /proc/uptime'),encoding='utf-8')
print('RETAINED_MOBILE_AND_OTA_PAGES_CAPTURED_FOR_REVIEW',flush=True)
