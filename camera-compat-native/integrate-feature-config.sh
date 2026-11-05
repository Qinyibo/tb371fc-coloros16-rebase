#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
m="$r/camera-compat-native/mount-odm-feature"
mkdir -p "$m"
trap 'mountpoint -q "$m" && umount "$m" || true' EXIT
mount -t ext4 -o loop,rw "$r/integrated-network/odm-camera-feature.img" "$m"
python3 - "$r" "$m" <<'PY'
from pathlib import Path
import hashlib,json,os,stat,sys
r,m=map(Path,sys.argv[1:]);w=r/'camera-compat-native'
assert not (w/'odm-feature-integration.json').exists()
def snapshot(root):
    result={}
    for directory,dirs,files in os.walk(root,followlinks=False):
        for name in sorted(dirs+files):
            p=Path(directory)/name;s=p.lstat()
            attrs={k:os.getxattr(p,k,follow_symlinks=False).hex() for k in os.listxattr(p,follow_symlinks=False)}
            data=hashlib.file_digest(p.open('rb'),'sha256').hexdigest() if stat.S_ISREG(s.st_mode) else (os.readlink(p) if stat.S_ISLNK(s.st_mode) else None)
            result[p.relative_to(root).as_posix()]=[s.st_mode,s.st_uid,s.st_gid,attrs,data]
    return result
before=snapshot(m)
relative='etc/camera/config/camera_unit_feature_config.protobuf';dest=m/relative
assert not dest.exists()
src=w/'config-donor/camera_unit_feature_config.protobuf';data=src.read_bytes()
assert len(data)==17962 and hashlib.sha256(data).hexdigest()=='b1b31f53c8347bf28b238b9e881786ef77adb051aef8d5b0fd678bb4d425d339'
created=[]
for parent in [m/'etc',m/'etc/camera',m/'etc/camera/config']:
    if parent.exists():continue
    parent.mkdir();os.chmod(parent,0o755);os.chown(parent,0,0)
    os.setxattr(parent,'security.selinux',b'u:object_r:vendor_configs_file:s0')
    created.append(parent.relative_to(m).as_posix())
dest.write_bytes(data);os.chmod(dest,0o644);os.chown(dest,0,0)
os.setxattr(dest,'security.selinux',b'u:object_r:vendor_configs_file:s0')
after=snapshot(m)
assert all(after.get(k)==v for k,v in before.items()),'An existing TB BSP entry changed'
assert set(after)-set(before)==set(created+[relative])
result={'state':'BUILT_NOT_PHYSICALLY_VERIFIED','source_donor':'OPD2413_16.0.10.600(CN01)',
        'only_new_file':relative,'file_sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),
        'added_directories':created,'all_previous_bsp_entries_identical':True,'previous_entries_checked':len(before),
        'before_image_sha256':'eec06da5d0fbab6808028cc7341a495ed810de30b7f931db988ca664a9525a17',
        'scope':'Unmodified same-release camera application feature definitions. No HAL, firmware, calibration, existing BSP files or feature-success stubs changed.',
        'camera_runtime_pass':False}
(w/'odm-feature-integration.json').write_text(json.dumps(result,indent=2)+'\n')
print('CAMERA_FEATURE_DEFINITIONS_ADDED_ALL_PREVIOUS_BSP_ENTRIES_EXACT',len(before))
PY
umount "$m"
e2fsck -fn "$r/integrated-network/odm-camera-feature.img" > "$r/camera-compat-native/odm-feature-fsck.log" 2>&1
python3 - "$r" <<'PY'
from pathlib import Path
import hashlib,json,sys
r=Path(sys.argv[1]);p=r/'camera-compat-native/odm-feature-integration.json';x=json.loads(p.read_text())
x['after_image_sha256']=hashlib.file_digest((r/'integrated-network/odm-camera-feature.img').open('rb'),'sha256').hexdigest()
x['filesystem_check_pass']=True;p.write_text(json.dumps(x,indent=2)+'\n');print('ODM_CAMERA_FEATURE_FILESYSTEM_PASS',x['after_image_sha256'])
PY
