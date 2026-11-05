#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/ui-compat/native-ui/tablet-viewport-v6r2"
m="$w/mount"
old="$r/integrated-network/system_ext-stack-v4-package-info.img"
new="$r/integrated-network/system_ext-tablet-viewport-v6r2.img"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
test ! -e "$new"
test "$(sha256sum "$old" | cut -d' ' -f1)" = 927b25dfa131db61f160b7a91b279146f4df6bdf1e4a7356ed875e62906f33df
cp --reflink=auto --sparse=always "$old" "$new"
mkdir -p "$m"
trap 'if mountpoint -q "$m"; then umount "$m"; fi' EXIT
mount -t ext4 -o loop,rw "$new" "$m"
python3 - "$w" "$m" <<'PY'
from pathlib import Path
import hashlib,json,os,sys
work,mount=map(Path,sys.argv[1:])
p=mount/"priv-app/OplusLauncher/OplusLauncher.apk"
old=p.read_bytes();data=(work/"build/OplusLauncher.apk").read_bytes()
record=json.loads((work/"build.json").read_bytes())
digest=lambda b:hashlib.sha256(b).hexdigest()
assert digest(old)==record["source_sha256"] and digest(data)==record["apk_sha256"]
def attrs(p):
 s=p.stat();return (s.st_uid,s.st_gid,s.st_mode,{n:os.getxattr(p,n) for n in os.listxattr(p)})
before=attrs(p);p.write_bytes(data)
assert attrs(p)==before and p.read_bytes()==data
(work/"integration.json").write_text(json.dumps({
 "only_replaced_file":"priv-app/OplusLauncher/OplusLauncher.apk",
 "before_sha256":digest(old),"after_sha256":digest(data),"owner_mode_xattrs_unchanged":True,
 "runtime_verified":False
},indent=2)+"\n")
PY
umount "$m"
e2fsck -fn "$new" > "$w/system_ext-fsck.log" 2>&1
