#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/ui-compat/native-ui/pad-layout-v5"
m="$w/mount"
old="$r/integrated-network/system-camera-unit-tb.img"
new="$r/integrated-network/system-pad-layout-v5.img"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
test ! -e "$new"
test "$(sha256sum "$old" | cut -d' ' -f1)" = 64c47c234593b62d1561c624203ca0ec2cfa84c1cc110ae6de18287dc7474922
cp --reflink=auto --sparse=always "$old" "$new"
mkdir -p "$m"
trap 'if mountpoint -q "$m"; then umount "$m"; fi' EXIT
mount -t ext4 -o loop,rw "$new" "$m"
python3 - "$m" "$w" <<'PY'
from pathlib import Path
import hashlib,json,os,re,sys
mount,work=map(Path,sys.argv[1:])
p=mount/"my_product/build.prop"
before=p.read_bytes()
assert hashlib.sha256(before).hexdigest()=="bceecc9b381e9853c00331927794337eeb371bdb48379af0c50de25eb4370335"
after=re.sub(rb"(?m)^ro\.sf\.lcd_density=380(?=\r?$)",b"ro.sf.lcd_density=360",before)
assert after!=before and after.replace(b"ro.sf.lcd_density=360",b"ro.sf.lcd_density=380")==before
s=p.stat();attrs={k:os.getxattr(p,k) for k in os.listxattr(p)}
p.write_bytes(after)
assert (p.stat().st_uid,p.stat().st_gid,p.stat().st_mode)==(s.st_uid,s.st_gid,s.st_mode)
assert attrs=={k:os.getxattr(p,k) for k in os.listxattr(p)}
(work/"density-integration.json").write_text(json.dumps({
 "only_file_changed":"my_product/build.prop","property":"ro.sf.lcd_density",
 "before":380,"after":360,"donor_density":420,"donor_ppi":315,
 "tb_reported_ppi":[273.309,272.91],"same_physical_scale_density":420*(273.309+272.91)/2/315,
 "before_sha256":hashlib.sha256(before).hexdigest(),"after_sha256":hashlib.sha256(after).hexdigest(),
 "grid_resources_unchanged":True,"font_scale_preference":1.15,"runtime_override_final":False
},indent=2)+"\n")
PY
umount "$m"
e2fsck -fn "$new" > "$w/system-fsck.log" 2>&1
