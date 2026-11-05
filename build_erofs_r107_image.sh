#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
gitrepo=/mnt/d/TB371FC-release/public-source/android_kernel_lenovo_tb371fc.git
old=/work/tb371fc-wake-20261031/out
dst=/work/tb371fc-clean-rebase-r107-erofs-20261104
log="$r/erofs-kernel-build"
rev=41082098de91855a809239bf64f339a16d39effe
export PATH=/usr/lib/llvm-21/bin:$PATH LD_LIBRARY_PATH=/root/tc-shim/lib TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0
mkdir "$dst" "$log"
mkdir "$dst/src" "$dst/out"
src="$dst/src"; out="$dst/out"
echo "EXTRACT $rev"
git --git-dir="$gitrepo" archive "$rev" | tar -x -C "$src"
mv "$src/drivers/staging/erofs" "$dst/staging-erofs-baseline"
python3 "$r/apply_erofs_r107.py" "$r" "$src"
cp "$old/.config" "$out/.config"
"$src/scripts/config" --file "$out/.config" -e EROFS_FS -e EROFS_FS_XATTR -e EROFS_FS_POSIX_ACL -e EROFS_FS_SECURITY -e EROFS_FS_ZIP -d EROFS_FS_DEBUG -d EROFS_FS_PCPU_KTHREAD
export KBUILD_BUILD_USER=tb371fc-offline KBUILD_BUILD_HOST=r107-clean-erofs KBUILD_BUILD_TIMESTAMP='Sat Oct 31 2026 20:00:00 +0800' KBUILD_BUILD_VERSION=43
make_k() { make -C "$src" O="$out" ARCH=arm64 CC=clang CLANG_TRIPLE=aarch64-linux-gnu- CROSS_COMPILE=aarch64-linux-gnu- AS=aarch64-linux-gnu-as LOCALVERSION= DYNAMIC_SINGLE_CHIP=qca6390 "$@"; }
make_k olddefconfig > "$log/config.log" 2>&1
"$src/scripts/diffconfig" "$old/.config" "$out/.config" > "$log/config.diff"
cat "$log/config.diff"
python3 - "$log/config.diff" <<'PY'
import pathlib,sys
p=pathlib.Path(sys.argv[1]);lines=p.read_text().splitlines()
assert lines and all(x.lstrip(' +-').startswith('EROFS_FS') for x in lines),lines
PY
echo "BUILD $(nproc) CPUs (using 8)"
make_k -j8 KCFLAGS="-Wno-error -Wno-error=strict-prototypes -Wno-error=implicit-int -Wno-error=incompatible-pointer-types -Wno-error=date-time" Image modules > "$log/build.log" 2>&1
cp "$out/arch/arm64/boot/Image" "$out/Module.symvers" "$out/.config" "$log/"
sha256sum "$log/Image" "$log/Module.symvers" "$log/.config" > "$log/SHA256SUMS"
echo 'R107_EROFS_FULL_IMAGE_BUILT'
