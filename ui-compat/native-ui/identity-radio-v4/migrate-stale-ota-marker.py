"""One-time native Settings migration of an orphaned OTA corner indicator."""
from pathlib import Path
import json,shlex,subprocess,time
w=Path('ui-compat/native-ui/identity-radio-v4/ota-marker-migration')
w.mkdir(exist_ok=False)
a=['D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe','-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL']
def run(c):
 x=subprocess.run(a+['shell','/debug_ramdisk/su -c '+shlex.quote(c)],capture_output=True,timeout=25)
 assert x.returncode==0,(c,x.stderr)
 return x.stdout.decode(errors='replace').replace('\r','')
key='oplus_customize_ota_patch'
before=run('settings get system '+key).strip()
packages=run('content query --uri content://com.oplus.ota/pkgList')
assert packages.strip()=='No result found.',packages
assert before=='1',before
probe=json.loads(Path('ui-compat/native-ui/identity-radio-v4/ota-transport-v4/result.json').read_bytes())
assert probe['pinned_domain_observed']
backup={'namespace':'system','key':key,'before':before,'package_list_before':packages,'reason':'Original OTA package list is empty; obsolete corner indicator remains 1. Consumer defaults to 0; no update/query result is forged.','rollback_command':'settings put system '+key+' 1','continuous_marker_override':False,'applied':False}
(w/'migration.json').write_text(json.dumps(backup,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
deleted=run('settings delete system '+key)
backup['applied']=True
(w/'migration.json').write_text(json.dumps(backup,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
assert run('settings get system '+key).strip()=='null'
action=run('am broadcast -a oplus.intent.ota.OTA_CHECK_NEW_VERSION_UPDATE -n com.oplus.ota/com.oplus.ota.strategy.StrategyReceiver --es query_update_mode manual')
time.sleep(6)
after=run('settings get system '+key).strip()
after_packages=run('content query --uri content://com.oplus.ota/pkgList')
result={'before':before,'delete_action':deleted,'manual_native_check':action,'after':after,'package_list_after':after_packages,'native_effective_indicator':0 if after=='null' else int(after),'ui_verified':False,'server_latest_claimed':False,'no_update_result_forged':True}
(w/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
assert after in ['null','0'] and after_packages.strip()=='No result found.',result
print('STALE_NATIVE_INDICATOR_REMOVED_ONCE_MANUAL_QUERY_HAS_NO_CANDIDATE')
