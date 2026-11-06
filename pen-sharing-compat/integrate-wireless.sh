#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/pen-sharing-compat"
old="$r/integrated-network/system_ext-identity-radio-v4.img"
new="$w/system_ext-pen-v1.img"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
test ! -e "$new"
test "$(sha256sum "$old" | cut -d' ' -f1)" = a52793eff6eeee3d5cbf22ff57b50b3aeee9d7fb773d45b7ccfd1f1f76c75c3f
cp --reflink=auto --sparse=always "$old" "$new"
mkdir -p "$w/ext-mount"
trap 'if mountpoint -q "$w/ext-mount"; then umount "$w/ext-mount"; fi' EXIT
mount -t ext4 -o loop,rw,noatime "$new" "$w/ext-mount"
python3 - "$w" <<'PY'
from pathlib import Path
import hashlib,json,os,stat,sys
w=Path(sys.argv[1]);m=w/'ext-mount';row=json.loads((w/'build/pen-build-result.json').read_text())['WirelessSettings-current.apk'];sha=lambda p:hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
p=m/'priv-app/WirelessSettings/WirelessSettings.apk';assert sha(p)==row['input_sha256']
metadata=(p.stat().st_uid,p.stat().st_gid,stat.S_IMODE(p.stat().st_mode),{n:os.getxattr(p,n).hex() for n in os.listxattr(p)})
p.write_bytes((w/row['output']).read_bytes());assert sha(p)==row['output_sha256']
assert metadata==(p.stat().st_uid,p.stat().st_gid,stat.S_IMODE(p.stat().st_mode),{n:os.getxattr(p,n).hex() for n in os.listxattr(p)})
removed=[]
for q in [p.with_name(p.name+'.fsv_meta'),p.with_name(p.name+'.prof'),p.with_name(p.name+'.prof.fsv_meta'),*list((p.parent/'oat').rglob('*'))]:
 if q.is_file() and (q.parent==p.parent or q.name.startswith('WirelessSettings.')):removed.append(str(q.relative_to(m)));q.unlink()
(w/'pen-ext-integration.json').write_text(json.dumps({'file':str(p.relative_to(m)),'input_sha256':row['input_sha256'],'output_sha256':row['output_sha256'],'removed_stale_sidecars':removed,'metadata_preserved':True,'filesystem_check_pass':False,'physical_verified':False},indent=2)+'\n')
print('WIRELESS_PEN_CLASSIFICATION_INTEGRATED',flush=True)
PY
umount "$w/ext-mount"
e2fsck -fn "$new" > "$w/system-ext-fsck.log" 2>&1
python3 - "$w" "$new" <<'PY'
from pathlib import Path
import hashlib,json,sys
w,p=map(Path,sys.argv[1:]);f=w/'pen-ext-integration.json';d=json.loads(f.read_text());d['filesystem_check_pass']=True
with p.open('rb') as s:d['after_image_sha256']=hashlib.file_digest(s,'sha256').hexdigest()
f.write_text(json.dumps(d,indent=2)+'\n');print('WIRELESS_PEN_FSCK_PASS',d['after_image_sha256'],flush=True)
PY
