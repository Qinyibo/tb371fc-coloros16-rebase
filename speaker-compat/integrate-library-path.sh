#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
m="$r/speaker-compat/mount-system_ext"
trap 'mountpoint -q "$m" && umount "$m" || true' EXIT
mount -t ext4 -o loop,rw "$r/integrated-network/system_ext-speaker.img" "$m"
python3 - "$r" "$m" <<'PY'
from pathlib import Path
import hashlib,json,os,sys
r,m=map(Path,sys.argv[1:]);sha=lambda p:hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
old=m/'etc/tb371fc-speaker/direction.so';new=m/'lib64/libtb371fc_speaker.so'
assert sha(old)=='c32f9b49c8a1e4aadd06ea72bcefdc8283f321c71a06a14d7e0b4a705f4aa675'
assert not new.exists()
old.rename(new)
assert new.stat().st_mode & 0o777 == 0o644 and new.stat().st_uid==new.stat().st_gid==0
assert os.getxattr(new,'security.selinux')==b'u:object_r:system_file:s0'
p=m/'etc/tb371fc-speaker/start.sh';st=p.stat();attrs={n:os.getxattr(p,n) for n in os.listxattr(p)}
p.write_bytes((r/'speaker-compat/start.sh').read_bytes())
assert (p.stat().st_mode,p.stat().st_uid,p.stat().st_gid)==(st.st_mode,st.st_uid,st.st_gid)
assert attrs=={n:os.getxattr(p,n) for n in os.listxattr(p)}
assert sha(m/'etc/tb371fc-speaker/direction.jar')=='d11f3cf3e9fb8739c1a25c2e48a5cd266a4f07a1d97fdf3b820d606bfe835add'
assert sha(m/'etc/tb371fc-speaker/directionctl')=='a4cdf0686a98d8dc455b3543b8bb71c27d3bef0b74d538c9741645ff67b7d679'
(r/'speaker-compat/library-path-integration.json').write_text(json.dumps({'change':'Move unchanged JNI binary into system_ext/lib64 and declare the process native library search path','library_sha256':sha(new),'wrapper_sha256':sha(p),'java_jni_and_driver_unchanged':True,'restart_loop_added':False,'physical_verified':False},indent=2)+'\n')
PY
umount "$m"
e2fsck -fn "$r/integrated-network/system_ext-speaker.img" > "$r/speaker-compat/system_ext-speaker-fsck.log" 2>&1
echo SPEAKER_LIBRARY_PATH_FILESYSTEM_PASS
