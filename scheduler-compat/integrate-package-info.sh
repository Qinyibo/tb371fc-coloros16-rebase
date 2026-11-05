#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
m="$r/speaker-compat/mount-system_ext"
old="$r/integrated-network/system_ext-stack-v4.img"
new="$r/integrated-network/system_ext-stack-v4-package-info.img"
test ! -e "$new"
test "$(sha256sum "$old" | cut -d ' ' -f 1)" = e5938b39d4025dc5900a63cf534be44097eb46114778d084790321f924b33050
cp --sparse=always "$old" "$new"
mount -t ext4 -o loop,rw,noatime "$new" "$m"
trap 'mountpoint -q "$m" && umount "$m" || true' EXIT
p="$m/etc/init/tb371fc-scheduler.rc"
test "$(sha256sum "$p" | cut -d ' ' -f 1)" = 74be54ecc42097490bb47c12f45edc77543ccc8faf0479e6aac756a3e7504ad1
python3 - "$p" "$r/scheduler-compat/tb371fc-scheduler.rc" <<'PY'
from pathlib import Path
import sys,os
p,s=map(Path,sys.argv[1:]);before=p.read_bytes();after=s.read_bytes();a=b'group root system readproc';b=a+b' package_info';assert before.count(a)==1 and before.replace(a,b)==after
st=p.stat();x=os.getxattr(p,'security.selinux');p.write_bytes(after);assert (st.st_mode,st.st_uid,st.st_gid)==(p.stat().st_mode,p.stat().st_uid,p.stat().st_gid);assert x==os.getxattr(p,'security.selinux')
PY
umount "$m"
e2fsck -fn "$new" > "$r/scheduler-compat/package-info-fsck.log" 2>&1
sha256sum "$new"
