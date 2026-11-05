"""Read real boot identity and the unmodified WeChat login-selection screen."""
from pathlib import Path
import hashlib,json,shlex,subprocess,time,xml.etree.ElementTree as ET
w=Path('ui-compat/native-ui/brand-consistency-v5');out=w/'runtime';out.mkdir(exist_ok=False)
a=['D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe','-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL']
def run(c,root=False,timeout=25):
 x=subprocess.run(a+['shell',('/debug_ramdisk/su -c '+shlex.quote(c)) if root else c],capture_output=True,timeout=timeout)
 assert x.returncode==0,(c,x.stdout[-800:],x.stderr)
 return x.stdout.decode(errors='replace').replace('\r','')
def snap(name):
 x=subprocess.run(a+['exec-out','screencap -p'],capture_output=True,check=True,timeout=15)
 assert x.stdout.startswith(b'\x89PNG');(out/(name+'.png')).write_bytes(x.stdout)
 run('uiautomator dump /data/local/tmp/tb371fc-brand-v5.xml')
 xml=run('cat /data/local/tmp/tb371fc-brand-v5.xml')
 (out/(name+'.xml')).write_text(xml,encoding='utf8')
 return [n.get('text') for n in ET.fromstring(xml).iter('node') if n.get('text')]
subprocess.run(a+['wait-for-device'],check=True,timeout=90)
for attempt in range(12):
 if run('getprop sys.boot_completed').strip()=='1':break
 time.sleep(5)
else:raise RuntimeError('Boot did not complete within bounded check')
expected={'ro.product.brand':'Lenovo','ro.product.model':'TB371FC','ro.product.manufacturer':'LENOVO','ro.product.cpuinfo':'SM8250_AC','ro.soc.model':'SM8250-AC','ro.vendor.oplus.market.name':'小新Pad Pro 12.7','ro.product.cpu.abi':'arm64-v8a'}
identity={k:run('getprop '+k).strip() for k in expected}
(out/'identity.json').write_text(json.dumps(identity,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
assert identity==expected,identity
assert run('getenforce').strip()=='Enforcing'
assert '9af2253db09e409598632b24ddec34f848f781c2467683133ddc655abd49f015' in run('sha256sum /my_manifest/build.prop',True)
before=run('cat /proc/sys/kernel/random/boot_id; pidof system_server; pidof com.android.launcher; pidof com.android.phone; cat /proc/uptime')
(out/'before.txt').write_text(before,encoding='utf8')
assert 'secure=false' in run('dumpsys window policy | grep -m1 secure=')
try:
 run('input keyevent KEYCODE_WAKEUP; wm dismiss-keyguard')
 launch=run('am start -W -n com.tencent.mm/com.tencent.mm.plugin.account.ui.LoginSelectUI',True)
 (out/'wechat-launch.txt').write_text(launch,encoding='utf8')
 assert 'Error:' not in launch and 'Permission Denial' not in launch,launch
 time.sleep(8)
 labels=snap('wechat-login-selection')
 if 'USB 用于' in labels:
  run('input keyevent KEYCODE_BACK');labels=snap('wechat-login-selection-unblocked')
 simultaneous=any('同时登录' in s for s in labels)
 if not simultaneous:
  time.sleep(10);labels=snap('wechat-login-selection-late')
  simultaneous=any('同时登录' in s for s in labels)
 result={'identity_verified':True,'wechat_visible_text':labels,'simultaneous_login_entry_observed':simultaneous,'real_account_login_tested':False,'account_data_cleared':False,'wechat_apk_modified':False,'native_ui_function_only_no_performance_claim':True}
 (out/'wechat-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print(json.dumps(result,ensure_ascii=False),flush=True)
finally:
 run('input keyevent KEYCODE_HOME; input keyevent KEYCODE_SLEEP')
(out/'after.txt').write_text(run('cat /proc/sys/kernel/random/boot_id; pidof system_server; pidof com.android.launcher; pidof com.android.phone; cat /proc/uptime'),encoding='utf8')
