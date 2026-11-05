#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/ui-compat/native-ui/identity-radio-v4"
sold="$r/integrated-network/system-network-ota-retained-v3.img"
snew="$r/integrated-network/system-identity-radio-v4.img"
eold="$r/integrated-network/system_ext-network-ota-retained-v3.img"
enew="$r/integrated-network/system_ext-identity-radio-v4.img"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
test ! -e "$snew"; test ! -e "$enew"
test "$(sha256sum "$sold" | cut -d' ' -f1)" = ce6bbf7ac45f420678a4d397e4db199286919c581656c0ef19da229012942289
test "$(sha256sum "$eold" | cut -d' ' -f1)" = ec38c4b0bf9dfb26a1d5d8db634b0cd8bb31bf4d08a28d5c9490027b4b014ce0
cp --reflink=auto --sparse=always "$sold" "$snew"
cp --reflink=auto --sparse=always "$eold" "$enew"
mkdir -p "$w/system-mount" "$w/ext-mount"
trap 'for p in "$w/system-mount" "$w/ext-mount"; do if mountpoint -q "$p"; then umount "$p"; fi; done' EXIT
mount -t ext4 -o loop,rw "$snew" "$w/system-mount"
mount -t ext4 -o loop,rw "$enew" "$w/ext-mount"
python3 - "$r" "$w" <<'INNER'
from pathlib import Path
import hashlib,json,os,re,sys
r,w=map(Path,sys.argv[1:]);s=w/'system-mount';e=w/'ext-mount';sha=lambda b:hashlib.sha256(b).hexdigest();changes=[]
def attrs(p):
 t=p.stat();return (t.st_uid,t.st_gid,t.st_mode,{n:os.getxattr(p,n) for n in os.listxattr(p)})
def replace(p,after,base):
 before=p.read_bytes();st=attrs(p);p.write_bytes(after);assert attrs(p)==st
 changes.append({'file':str(p.relative_to(base)),'before_sha256':sha(before),'after_sha256':sha(after),'owner_mode_xattrs_preserved':True})
p=s/'my_manifest/build.prop';before=p.read_bytes();assert before==(r/'ui-compat/native-ui/network-ota-retained-v3/my-manifest-build.before.prop').read_bytes()
policy=json.loads((w/'native-identity-policy.json').read_bytes());after=before;edits=[]
for key,value in policy['replace_existing'].items():
 pattern=rb'(?m)^'+re.escape(key.encode())+rb'=([^\r\n]*)'
 m=re.search(pattern,after);assert m is not None,key
 edits.append({'property':key,'before':m.group(1).decode(),'after':value})
 after,count=re.subn(pattern,lambda m:key.encode()+b'='+value.encode(),after);assert count==1,key
for key,value in policy['add_native_variant_properties'].items():
 assert re.search(rb'(?m)^'+re.escape(key.encode())+b'=',after) is None
 after+=key.encode()+b'='+value.encode()+b'\n'
 edits.append({'property':key,'before':None,'after':value})
replace(p,after,s)
p=e/'framework/oplus-telephony-common.jar';assert sha(p.read_bytes())=='7455cb251c4ebf4c1685351e69ee3d150c8bb586e46916c17f6bb86c5e5ce737'
radio=json.loads((w/'radio-build.json').read_bytes());data=(w/'build/oplus-telephony-common.jar').read_bytes();assert sha(data)==radio['output_sha256'];replace(p,data,e)
assert not (e/'framework/oat/arm64/oplus-telephony-common.odex').exists()
assert sha((e/'app/OTA/OTA.apk').read_bytes())=='4fc2b16c991195d8bd6a0b760678ea9e074f9450287475453ff79bd64224479f'
(w/'integration.json').write_text(json.dumps({'changes':changes,'native_identity_properties':edits,'radio_original_methods_changed':2,'radio_other_members_and_native_error_paths_unchanged':True,'kernel_vendor_hal_unchanged':True,'original_ota_app_retained':True,'native_update_endpoint_policy_retained':True,'no_runtime_identity_rewriter':True,'physical_verified':False},ensure_ascii=False,indent=2)+'\n')
print('TWO_OPTIONAL_RADIO_LOOKUPS_AND_NATIVE_TB_IDENTITY_INTEGRATED',flush=True)
INNER
umount "$w/system-mount"; umount "$w/ext-mount"
e2fsck -fn "$snew" > "$w/system-fsck.log" 2>&1
e2fsck -fn "$enew" > "$w/system_ext-fsck.log" 2>&1
printf 'BOTH_FILESYSTEM_CHECKS_PASS\n'
