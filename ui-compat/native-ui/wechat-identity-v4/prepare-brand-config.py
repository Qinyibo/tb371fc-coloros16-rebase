"""Save observed identity and prepare one native property correction offline."""
from pathlib import Path
import hashlib,json,shlex,subprocess
w=Path('ui-compat/native-ui/wechat-identity-v4')
adb=['D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe','-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL']
def read(command):
 x=subprocess.run(adb+['exec-out','/debug_ramdisk/su -c '+shlex.quote(command)],capture_output=True,timeout=25)
 assert x.returncode==0,(command,x.stderr)
 return x.stdout
keys=['ro.product.brand','ro.product.manufacturer','ro.product.model','ro.product.cpuinfo','ro.soc.model','ro.build.characteristics','ro.product.cpu.abi']
identity={k:read('getprop '+k).decode().strip() for k in keys}
(w/'observed-identity.json').write_text(json.dumps(identity,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
before=read('cat /my_manifest/build.prop')
sha=lambda d:hashlib.sha256(d).hexdigest()
assert sha(before)=='247dace493cbd74bbfa020295ffb05ee02ae4d3922e1f46c920ea34aaa127dfb'
assert b'\nro.product.brand=' not in before
assert before.endswith(b'\n')
after=before+b'ro.product.brand=Lenovo\n'
(w/'my-manifest-build.before.prop').write_bytes(before)
(w/'brand-consistency-candidate.prop').write_bytes(after)
record={
 'observed':identity,
 'wechat_apk_sha256':sha((w/'installed-original.apk').read_bytes()),
 'source_evidence':{
  'login_selection':'LoginSelectUI.onCreate hides phone_and_pad initially, passes lowercase Build.BRAND and model accessor + CPU_ABI to CheckLoginAsPad; callback shows entry only on true.',
  'server_query':'l41/j1.a sends brand/model to /cgi-bin/micromsg-bin/checkloginaspad; failure or LoginAsPad=false produces false.',
  'cpu_display_property':'No DEX string reference to ro.product.cpuinfo; ro.soc.model references found outside the inspected login path.',
  'tablet_environment':'Native ok.C supports OEM tablet features and widthDp >= 600 fallback.'
 },
 'confirmed_defect':'Generic brand remains OnePlus while model/manufacturer are TB371FC/LENOVO after V4 identity change.',
 'wechat_failure_cause':'Not proven: current server response not captured; mixed identity is a concrete candidate cause, not proof of rejection.',
 'offline_change':{'file':'my_manifest/build.prop','before_sha256':sha(before),'after_sha256':sha(after),'added_property':{'ro.product.brand':'Lenovo'},'all_prior_bytes_unchanged':True,'cpu_mapping_unchanged':True},
 'candidate_integrated':False,'device_modified_by_this_probe':False,'actual_dual_login_verified':False,
 'next':'Integrate truthful Lenovo brand consistently in native image; verify original WeChat entry without data wipe, application hooks or forged server results. Real account login remains user-operated.'
}
(w/'diagnosis.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'observed':identity,'offline_brand_candidate_sha256':sha(after),'wechat_cause_proven':False},ensure_ascii=False))
