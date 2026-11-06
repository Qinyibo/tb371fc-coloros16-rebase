#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/pen-sharing-compat"
old="$w/system-pen-v3.img"
new="$w/system-pen-v4.img"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
test ! -e "$new"
test "$(sha256sum "$old" | cut -d' ' -f1)" = 0b095d6adcf00e3636d5f0b5bc1a65756218cd1121a4d81bca714ca5e7b9a297
cp --reflink=auto --sparse=always "$old" "$new"
mkdir -p "$w/system-mount-v4"
trap 'if mountpoint -q "$w/system-mount-v4"; then umount "$w/system-mount-v4"; fi' EXIT
mount -t ext4 -o loop,rw,noatime "$new" "$w/system-mount-v4"
python3 - "$w" <<'PY'
from pathlib import Path
import hashlib,json,os,stat,sys
w=Path(sys.argv[1]);m=w/'system-mount-v4';d=json.loads((w/'build-v4/pen-build-result.json').read_text());sha=lambda p:hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
app=[p for p in [m/'my_product/priv-app/IPeManager/IPeManager.apk',m/'system/my_product/priv-app/IPeManager/IPeManager.apk'] if p.is_file()]
assert len(app)==1,app
jar=m/'system/framework/services.jar';assert jar.is_file()
removed=[];files=[]
for key,p in [('IPeManager-current.apk',app[0]),('services-current.jar',jar)]:
 row=d[key];expected={'IPeManager-current.apk':'e3d1fb14e6cab68fbdeae88dc266f59079139419fcf42e37f3398bceacc4d4b2','services-current.jar':'6c14c481685073a5dd48126397c2d7834d90739145f3b0b65bd4410013319c7c'}[key];assert sha(p)==expected,(str(p),sha(p),expected)
 metadata=(p.stat().st_uid,p.stat().st_gid,stat.S_IMODE(p.stat().st_mode),{n:os.getxattr(p,n).hex() for n in os.listxattr(p)})
 p.write_bytes((w/row['output'].replace('\\','/')).read_bytes());assert sha(p)==row['output_sha256']
 assert metadata==(p.stat().st_uid,p.stat().st_gid,stat.S_IMODE(p.stat().st_mode),{n:os.getxattr(p,n).hex() for n in os.listxattr(p)})
 files.append({'path':str(p.relative_to(m)),**row})
 # Remove only stale verification/profile/AOT sidecars for the two changed owners.
 for side in [p.with_name(p.name+'.fsv_meta'),p.with_name(p.name+'.prof'),p.with_name(p.name+'.prof.fsv_meta')]:
  if side.is_file():removed.append(str(side.relative_to(m)));side.unlink()
 oat=p.parent/'oat'
 if oat.is_dir():
  stem=p.stem
  for q in oat.rglob('*'):
   if q.is_file() and (q.name.startswith(stem+'.') or q.name.startswith(stem+'-')):removed.append(str(q.relative_to(m)));q.unlink()
(w/'pen-v4-integration.json').write_text(json.dumps({'files':files,'removed_stale_sidecars':removed,'replacement_metadata_preserved':True,'filesystem_check_pass':False,'physical_boot_verified':False,'pen_hardware_verified':False},indent=2)+'\n')
print('PEN_SYSTEM_PRELOADS_INTEGRATED',len(files),'STALE_OWNER_SIDECARS_REMOVED',len(removed),flush=True)
PY
umount "$w/system-mount-v4"
e2fsck -fn "$new" > "$w/system-v4-fsck.log" 2>&1
python3 - "$w" "$new" <<'PY'
from pathlib import Path
import hashlib,json,sys
w,p=map(Path,sys.argv[1:]);f=w/'pen-v4-integration.json';d=json.loads(f.read_text());d['filesystem_check_pass']=True
with p.open('rb') as s:d['after_image_sha256']=hashlib.file_digest(s,'sha256').hexdigest()
f.write_text(json.dumps(d,indent=2)+'\n');print('PEN_SYSTEM_FSCK_PASS',d['after_image_sha256'],flush=True)
PY
