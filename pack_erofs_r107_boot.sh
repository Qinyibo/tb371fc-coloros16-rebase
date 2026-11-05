#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
old=/work/tb371fc-wake-20261031/out
k="${1:-$r/erofs-kernel-build}"
out="${2:-$r/boot-cleanbase-erofs}"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
mkdir -p "$out/work" "$out/readback"; test ! -e "$out/boot-a-OFFLINE.img"
python3 "$r/verify_kernel_abi.py" "$r" "$old" "$k"
cd "$out/work"
m="$r/boot-audit/magiskboot"
orig="$r/boot-cleanbase/boot-r107-cleanbase.img"
"$m" unpack "$orig" > "$out/unpack.log" 2>&1
cmp kernel "$r/boot-audit/kernel"
cp "$k/Image" kernel
"$m" repack "$orig" "$out/boot-a-OFFLINE.img" > "$out/repack.log" 2>&1
cd "$out/readback"
"$m" unpack "$out/boot-a-OFFLINE.img" > "$out/readback.log" 2>&1
cmp kernel "$k/Image"
cmp ramdisk.cpio "$r/boot-cleanbase/readback/ramdisk.cpio"
cmp dtb "$r/boot-audit/dtb"
python3 - "$out" "$orig" <<'PY'
import hashlib,json,pathlib,struct,sys
o,old=map(pathlib.Path,sys.argv[1:])
new=o/'boot-a-OFFLINE.img'
a=bytearray(old.open('rb').read(4096)); b=bytearray(new.open('rb').read(4096))
assert new.stat().st_size==old.stat().st_size==100663296
assert struct.unpack_from('<I',b,8)[0]==(o/'readback/kernel').stat().st_size
for start,end in ((8,12),(576,608),(1636,1644)):
 a[start:end]=b[start:end]=b'\0'*(end-start)
assert a==b,'Unexpected boot header differences'
with new.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
with (o/'readback/kernel').open('rb') as f:kernel_sha=hashlib.file_digest(f,'sha256').hexdigest()
(o/'result.json').write_text(json.dumps(dict(scope='Offline integrated r107 EROFS boot; never run on tablet',sha256=sha,kernel_sha256=kernel_sha,bytes=new.stat().st_size,dtb_and_clean_ramdisk_exact=True,boot_header_invariants=True,device_boot_tested=False),indent=2)+'\n')
print('BOOT_READBACK_PASS',sha)
PY
