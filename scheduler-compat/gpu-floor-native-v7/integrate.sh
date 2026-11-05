#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/scheduler-compat/gpu-floor-native-v7"
old="$r/integrated-network/vendor-wifi-profile-v1.img"
new="$r/integrated-network/vendor-gpu-floor-v7.img"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
test ! -e "$new"
test "$(sha256sum "$old" | cut -d' ' -f1)" = a93f4d5c0a0f5858b3322cc5dc4c888ac6b235bc1221c729150a092946aee257
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
before=inventory();rel='etc/init/tb371fc-gpu-profile.rc';p=m/rel;assert not p.exists()
payload=(w/'tb371fc-gpu-profile.rc').read_bytes()
assert payload.count(b'    write ')==1 and payload.endswith(b'    write /sys/class/kgsl/kgsl-3d0/min_pwrlevel 4\n')
template=m/'etc/init/hw/init.qcom.rc';s=template.stat();p.write_bytes(payload);os.chown(p,s.st_uid,s.st_gid);os.chmod(p,stat.S_IMODE(s.st_mode))
for n in os.listxattr(template):os.setxattr(p,n,os.getxattr(template,n))
after=inventory();assert set(after)-set(before)=={rel} and not(set(before)-set(after))
assert all(after[k]==v for k,v in before.items())
(w/'gpu-profile-integration.json').write_text(json.dumps({'only_new_file':rel,'new_file_sha256':sha(payload),'only_driver_parameter':'/sys/class/kgsl/kgsl-3d0/min_pwrlevel','value':'4','boot_signal':'vendor.post_boot.parsed=1','board_guard':'spinel','all_previous_entries_identical':True,'entries_checked':len(before),'new_file_uses_existing_vendor_init_metadata':True,'before_image_sha256':'a93f4d5c0a0f5858b3322cc5dc4c888ac6b235bc1221c729150a092946aee257','filesystem_check_pass':False,'runtime_verified':False,'performance_verified':False},indent=2)+'\n')
print('ONE_NATIVE_VENDOR_GPU_PROFILE_ADDED_PREVIOUS_ENTRIES_IDENTICAL',len(before),flush=True)
PY
umount "$w/mount"
e2fsck -fn "$new" > "$w/vendor-fsck.log" 2>&1
python3 - "$w" "$new" <<'PY'
from pathlib import Path
import hashlib,json,sys
w,p=map(Path,sys.argv[1:]);f=w/'gpu-profile-integration.json';d=json.loads(f.read_bytes())
with p.open('rb') as s:d['after_image_sha256']=hashlib.file_digest(s,'sha256').hexdigest()
d['filesystem_check_pass']=True;f.write_text(json.dumps(d,indent=2)+'\n')
print('FILESYSTEM_CHECK_PASS',d['after_image_sha256'],flush=True)
PY
