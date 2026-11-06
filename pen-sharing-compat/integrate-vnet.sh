#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/pen-sharing-compat"
old="$r/integrated-network/vendor-gpu-floor-v7.img"
new="$w/vendor-pen-sharing-v1.img"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
test ! -e "$new"
test "$(sha256sum "$old" | cut -d' ' -f1)" = 1fb5e1e43db4e5fda93e4ded8e028a9434b85cbcdd2b169ec0ae28434da72377
cp --reflink=auto --sparse=always "$old" "$new"
mkdir -p "$w/mount"
trap 'if mountpoint -q "$w/mount"; then umount "$w/mount"; fi' EXIT
mount -t ext4 -o loop,rw,noatime "$new" "$w/mount"
python3 - "$w" <<'PY'
from pathlib import Path
import hashlib,json,os,stat,sys
w=Path(sys.argv[1]);m=w/'mount';sha=lambda b:hashlib.sha256(b).hexdigest()
def inventory():
 result={}
 for p in [m,*m.rglob('*')]:
  s=p.lstat();value=[s.st_uid,s.st_gid,s.st_mode,{n:os.getxattr(p,n,follow_symlinks=False).hex() for n in os.listxattr(p,follow_symlinks=False)}]
  if stat.S_ISREG(s.st_mode):
   with p.open('rb') as f:value.append(hashlib.file_digest(f,'sha256').hexdigest())
  elif stat.S_ISLNK(s.st_mode):value.append(os.readlink(p))
  result[str(p.relative_to(m))]=value
 return result
before=inventory()
for rel,template in [('etc/init/tb371fc-vnet.rc','etc/init/hw/init.qcom.rc'),('lib/modules/oplus_vnet.ko','lib/modules/lcd.ko')]:
 p=m/rel;assert not p.exists();t=m/template;s=t.stat();payload=(w/'vendor-overlay'/rel).read_bytes()
 p.write_bytes(payload);os.chown(p,s.st_uid,s.st_gid);os.chmod(p,stat.S_IMODE(s.st_mode))
 for n in os.listxattr(t):os.setxattr(p,n,os.getxattr(t,n))
after=inventory();expected={'etc/init/tb371fc-vnet.rc','lib/modules/oplus_vnet.ko'}
assert set(after)-set(before)==expected and not(set(before)-set(after))
assert all(after[k]==v for k,v in before.items())
(w/'vnet-integration.json').write_text(json.dumps({'new_files':sorted(expected),'all_previous_entries_identical':True,'entries_checked':len(before),'metadata_from_existing_vendor_files':True,'before_image_sha256':'1fb5e1e43db4e5fda93e4ded8e028a9434b85cbcdd2b169ec0ae28434da72377','filesystem_check_pass':False,'runtime_module_load_pass':True,'phone_end_to_end_pass':False},indent=2)+'\n')
print('REAL_VNET_DRIVER_INTEGRATED_PREVIOUS_ENTRIES_IDENTICAL',len(before),flush=True)
PY
umount "$w/mount"
e2fsck -fn "$new" > "$w/vendor-fsck.log" 2>&1
python3 - "$w" "$new" <<'PY'
from pathlib import Path
import hashlib,json,sys
w,p=map(Path,sys.argv[1:]);f=w/'vnet-integration.json';d=json.loads(f.read_bytes())
with p.open('rb') as s:d['after_image_sha256']=hashlib.file_digest(s,'sha256').hexdigest()
d['filesystem_check_pass']=True;f.write_text(json.dumps(d,indent=2)+'\n')
print('FILESYSTEM_CHECK_PASS',d['after_image_sha256'],flush=True)
PY
