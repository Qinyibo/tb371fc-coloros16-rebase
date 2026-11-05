#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/ui-compat/native-ui/network-ota-retained-v3"
sold="$r/integrated-network/system-wifi-capabilities-v2.img"
snew="$r/integrated-network/system-network-ota-retained-v3.img"
eold="$r/integrated-network/system_ext-recents-header-v8.img"
enew="$r/integrated-network/system_ext-network-ota-retained-v3.img"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
test ! -e "$snew"; test ! -e "$enew"
test "$(sha256sum "$sold" | cut -d' ' -f1)" = 0278188908e97b0f05cdf211210d9ec88244054d7288ede9be41cb6d3d8747b2
test "$(sha256sum "$eold" | cut -d' ' -f1)" = 91ac59b184155bb7add3298920db1d48e07a3f9a25475707ba6c67301578e71e
cp --reflink=auto --sparse=always "$sold" "$snew"
cp --reflink=auto --sparse=always "$eold" "$enew"
mkdir -p "$w/system-mount" "$w/ext-mount" "$w/original-ext-mount"
trap 'for p in "$w/system-mount" "$w/ext-mount" "$w/original-ext-mount"; do if mountpoint -q "$p"; then umount "$p"; fi; done' EXIT
mount -t ext4 -o loop,rw "$snew" "$w/system-mount"
mount -t ext4 -o loop,rw "$enew" "$w/ext-mount"
mount -t ext4 -o loop,ro,noload "$eold" "$w/original-ext-mount"
python3 - "$r" "$w" <<'INNER'
from pathlib import Path
import hashlib,json,os,re,shutil,sys,xml.etree.ElementTree as ET
r,w=map(Path,sys.argv[1:]);s=w/'system-mount';e=w/'ext-mount';sha=lambda b:hashlib.sha256(b).hexdigest();changes=[]
def attrs(p):
 t=p.lstat();return [t.st_uid,t.st_gid,t.st_mode,{n:os.getxattr(p,n,follow_symlinks=False) for n in os.listxattr(p,follow_symlinks=False)}]
def replace(p,data,base):
 before=p.read_bytes();st=attrs(p);p.write_bytes(data);assert attrs(p)==st
 changes.append({'file':str(p.relative_to(base)),'before_sha256':sha(before),'after_sha256':sha(data),'owner_mode_xattrs_preserved':True})
p=s/'my_product/etc/extension/com.oplus.oplus-feature.xml';before=p.read_bytes();original=(r/'ui-compat/native-ui/settings-network-update-v1/oplus-feature.before.xml').read_bytes()
flags=['oplus.software.radio.virtualmodem_support','oplus.software.radio.virtualmodem_cellinfo'];t=original
for flag in flags:
 t,count=re.subn(rb'(?m)^[ \t]*<oplus-feature name="'+re.escape(flag.encode())+rb'"/>\r?\n',b'',t);assert count==1
assert before==t
replace(p,original,s)
p=s/'my_stock/etc/extension/com.oplus.app-features.xml';before=p.read_bytes();assert before==(w/'stock-app-features.before.xml').read_bytes()
policy=json.loads((w/'endpoint-policy.json').read_bytes());after=before;endpoints=[]
for key in policy['keys']:
 pattern=rb'(<app_feature name="'+re.escape(key.encode())+rb'" args="String:)([^"]+)("/>)'
 match=re.search(pattern,after);assert match is not None,key
 endpoints.append({'key':key,'before':match.group(2).decode(),'after':policy['endpoint']})
 after,count=re.subn(pattern,lambda m:m.group(1)+policy['endpoint'].encode()+m.group(3),after);assert count==1
ET.fromstring(after)
replace(p,after,s)
p=e/'framework/oplus-telephony-common.jar';radio=json.loads((w/'radio-build.json').read_bytes());assert sha(p.read_bytes())==radio['source_sha256'];data=(w/'build/oplus-telephony-common.jar').read_bytes();assert sha(data)==radio['output_sha256'];replace(p,data,e)
# Remove only stale artifacts derived from this exact modified framework.
removed=[]
for relative in ['framework/oplus-telephony-common.jar.fsv_meta','framework/oat/arm64/oplus-telephony-common.odex','framework/oat/arm64/oplus-telephony-common.odex.fsv_meta','framework/oat/arm64/oplus-telephony-common.vdex','framework/oat/arm64/oplus-telephony-common.vdex.fsv_meta']:
 p=e/relative
 if p.is_file():removed.append({'file':relative,'sha256':sha(p.read_bytes())});p.unlink()
# Restore the exact OEM OTA directory from the pre-exclusion ext image.
# The source is an existing verified full image; no APK rebuild/signature change.
source_image=r/'integrated-network/system_ext-tablet-viewport-v6r2.img'
assert not (e/'app/OTA').exists()
(w/'integration-stage.json').write_text(json.dumps({'changes':changes,'restored_native_features':flags,'endpoint_changes':endpoints,'radio_changed_methods':1,'removed_stale_radio_artifacts':removed,'ota_restore_pending':True},indent=2)+'\n')
print('RADIO_OPTIONAL_LOOKUP_AND_NATIVE_OTA_DESTINATIONS_INTEGRATED',flush=True)
INNER
umount "$w/original-ext-mount"
mount -t ext4 -o loop,ro,noload "$r/integrated-network/system_ext-tablet-viewport-v6r2.img" "$w/original-ext-mount"
cp -a "$w/original-ext-mount/app/OTA" "$w/ext-mount/app/OTA"
python3 - "$w" <<'INNER'
from pathlib import Path
import hashlib,json,os,sys
w=Path(sys.argv[1]);src=w/'original-ext-mount/app/OTA';dst=w/'ext-mount/app/OTA'
def attrs(p):
 t=p.lstat();return (t.st_uid,t.st_gid,t.st_mode,{n:os.getxattr(p,n,follow_symlinks=False) for n in os.listxattr(p,follow_symlinks=False)})
assert attrs(src)==attrs(dst)
for a in src.rglob('*'):
 b=dst/a.relative_to(src);assert attrs(a)==attrs(b)
 if a.is_file():assert a.read_bytes()==b.read_bytes()
assert hashlib.sha256((dst/'OTA.apk').read_bytes()).hexdigest()=='4fc2b16c991195d8bd6a0b760678ea9e074f9450287475453ff79bd64224479f'
p=w/'integration-stage.json';d=json.loads(p.read_bytes());d['ota_restore_pending']=False;d['ota_oem_payload_byte_exact']=True;d['ota_owner_mode_xattrs_preserved']=True;d['physical_verified']=False;(w/'integration.json').write_text(json.dumps(d,indent=2)+'\n')
print('OEM_OTA_CLIENT_RESTORED_BYTE_EXACT',flush=True)
INNER
umount "$w/system-mount"; umount "$w/ext-mount"; umount "$w/original-ext-mount"
e2fsck -fn "$snew" > "$w/system-fsck.log" 2>&1
e2fsck -fn "$enew" > "$w/system_ext-fsck.log" 2>&1
printf 'BOTH_FILESYSTEM_CHECKS_PASS\n'
