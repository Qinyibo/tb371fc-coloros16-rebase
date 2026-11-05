#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
s="$r/ui-compat/mount-system"
e="$r/speaker-compat/mount-system_ext"
cleanup() {
    for m in "$s" "$e"; do
        if mountpoint -q "$m"; then umount "$m"; fi
    done
}
trap cleanup EXIT
mount -t ext4 -o loop,rw "$r/integrated-network/system-native-ui.img" "$s"
mount -t ext4 -o loop,rw "$r/integrated-network/system_ext-native-ui.img" "$e"
python3 - "$r" "$s" "$e" <<'PY'
from pathlib import Path
import hashlib,json,os,re,shutil,sys
r,s,e=map(Path,sys.argv[1:]);w=r/'ui-compat/native-ui'
assert not (w/'integration.json').exists()
rows=json.loads((w/'build/result.json').read_text())
checks=json.loads((w/'build/canonical-result.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
changes=[];removed=[]

def replace(path,data,expected):
    assert sha(path.read_bytes())==expected,str(path)
    st=path.stat();attrs={k:os.getxattr(path,k) for k in os.listxattr(path)}
    path.write_bytes(data)
    assert (path.stat().st_mode,path.stat().st_uid,path.stat().st_gid)==(st.st_mode,st.st_uid,st.st_gid)
    assert attrs=={k:os.getxattr(path,k) for k in os.listxattr(path)}
    changes.append({'path':str(path),'before_sha256':expected,'after_sha256':sha(data)})

locations={'launcher':e/'priv-app/OplusLauncher/OplusLauncher.apk',
           'settings':e/'priv-app/Settings/Settings.apk',
           'assistant':s/'my_stock/app/AssistantScreen/AssistantScreen.apk'}
for name,path in locations.items():
    info=rows[name];data=(r/info['output'].replace('\\','/')).read_bytes()
    assert sha(data)==info['sha256']==checks[name]['final_apk_sha256']
    assert checks[name]['only_expected_methods_and_helpers_changed']
    replace(path,data,info['input_sha256'])
    # ART must compile the new DEX normally. Never retain donor compiled code
    # or profiles for a changed APK, and never create a boot-time dexopt loop.
    folder=path.parent
    for item in list(folder.iterdir()):
        if item.name=='oat':
            assert not item.is_symlink() and item.resolve().is_relative_to(folder.resolve())
            removed.extend(str(p) for p in item.rglob('*') if p.is_file())
            shutil.rmtree(item)
        elif item.name in (path.name+'.prof',path.name+'.bprof'):
            assert item.is_file() and not item.is_symlink()
            removed.append(str(item));item.unlink()

p=s/'my_product/build.prop';before=p.read_bytes()
assert len(re.findall(rb'(?m)^persist\.sys\.oplus\.anim_level=1\r?$',before))==4
after=re.sub(rb'(?m)^persist\.sys\.oplus\.anim_level=1(?=\r?$)',b'persist.sys.oplus.anim_level=4',before)
replace(p,after,sha(before))
assert re.findall(rb'(?m)^ro\.sf\.lcd_density=(\d+)\r?$',after)==[b'340']
assert sha((s/'system/apex/com.android.wifi.apex').read_bytes())=='4327cb381edb918637bbece1af74f7f41bd764cb464a0c048b5571a34673f98e'
assert sha((s/'system/framework/oplus-services.jar').read_bytes())=='d17d7bfc4d0a0d8adc1a0b1147fa2aa5ff9f6d21f33513689e9ea7f7190c3737'
assert sha((e/'lib64/libtb371fc_speaker.so').read_bytes())=='c32f9b49c8a1e4aadd06ea72bcefdc8283f321c71a06a14d7e0b4a705f4aa675'
result={'changes':changes,'obsolete_compiled_files_removed':removed,'native_animation_default':4,
        'layout':'Original grid preserved; native viewport fit applies to this tablet image',
        'runtime_bootstrap_or_mounts_added':False,'physical_verified':False,
        'signing_scope':'Modified trusted-preload APKs retain original signer identity block; OEM cryptographic signatures are invalid after DEX changes. No signature-verification bypass patch added.'}
(w/'integration.json').write_text(json.dumps(result,indent=2)+'\n')
print('NATIVE_UI_FILES_INTEGRATED',len(changes),'obsolete_compiled_files_removed',len(removed))
PY
cleanup
e2fsck -fn "$r/integrated-network/system-native-ui.img" > "$r/ui-compat/native-ui/system-fsck.log" 2>&1
e2fsck -fn "$r/integrated-network/system_ext-native-ui.img" > "$r/ui-compat/native-ui/system_ext-fsck.log" 2>&1
echo NATIVE_UI_FILESYSTEM_PASS
