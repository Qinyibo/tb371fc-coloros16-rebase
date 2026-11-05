#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/ui-compat/native-ui/brand-consistency-v5"
old="$r/integrated-network/system-identity-radio-v4.img"
new="$r/integrated-network/system-brand-consistency-v5.img"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
test ! -e "$new"
mkdir -p "$w/system-mount"
test "$(sha256sum "$old" | cut -d' ' -f1)" = 55f169d7c09afa35c78cc6a9935fd3bbb1df4e4978eed3bc701368b683b2cca2
cp --reflink=auto --sparse=always "$old" "$new"
trap 'if mountpoint -q "$w/system-mount"; then umount "$w/system-mount"; fi' EXIT
mount -t ext4 -o loop,rw "$new" "$w/system-mount"
python3 - "$r" "$w" <<'PY'
from pathlib import Path
import hashlib,json,os,sys
r,w=map(Path,sys.argv[1:]);p=w/'system-mount/my_manifest/build.prop'
before=p.read_bytes();sha=lambda d:hashlib.sha256(d).hexdigest()
assert sha(before)=='247dace493cbd74bbfa020295ffb05ee02ae4d3922e1f46c920ea34aaa127dfb'
after=(r/'ui-compat/native-ui/wechat-identity-v4/brand-consistency-candidate.prop').read_bytes()
assert after==before+b'ro.product.brand=Lenovo\n'
def attributes(p):
 s=p.stat();return s.st_uid,s.st_gid,s.st_mode,{n:os.getxattr(p,n) for n in os.listxattr(p)}
previous=attributes(p);p.write_bytes(after);assert attributes(p)==previous
assert sha(p.read_bytes())=='9af2253db09e409598632b24ddec34f848f781c2467683133ddc655abd49f015'
(w/'integration.json').write_text(json.dumps({'file':'my_manifest/build.prop','before_sha256':sha(before),'after_sha256':sha(after),'added_property':{'ro.product.brand':'Lenovo'},'existing_property_bytes_unchanged':True,'owner_mode_xattrs_preserved':True,'runtime_scripts_added':False,'wechat_apk_changed':False,'runtime_verified':False},indent=2)+'\n')
print('NATIVE_BRAND_PROPERTY_INTEGRATED',flush=True)
PY
umount "$w/system-mount"
e2fsck -fn "$new" > "$w/system-fsck.log" 2>&1
echo FILESYSTEM_CHECK_PASS
