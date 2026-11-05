#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
log="$r/wifi-compat/kernel-build"
mkdir -p "$log"
dst=/work/tb371fc-clean-rebase-r107-erofs-20261104
src="$dst/src"; out="$dst/out"
export PATH=/usr/lib/llvm-21/bin:$PATH LD_LIBRARY_PATH=/root/tc-shim/lib TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
export KBUILD_BUILD_USER=tb371fc-offline KBUILD_BUILD_HOST=r107-clean-erofs KBUILD_BUILD_TIMESTAMP='Sat Oct 31 2026 20:00:00 +0800' KBUILD_BUILD_VERSION=43
flags='-Wno-error -Wno-error=strict-prototypes -Wno-error=implicit-int -Wno-error=incompatible-pointer-types -Wno-error=date-time'
make -C "$src" O="$out" ARCH=arm64 CC=clang CLANG_TRIPLE=aarch64-linux-gnu- CROSS_COMPILE=aarch64-linux-gnu- AS=aarch64-linux-gnu-as LOCALVERSION= DYNAMIC_SINGLE_CHIP=qca6390 -j10 KCFLAGS="$flags" Image modules > "$log/build-r2.log" 2>&1
cp "$out/arch/arm64/boot/Image" "$out/Module.symvers" "$out/.config" "$log/"
sha256sum "$log/Image" "$log/Module.symvers" "$log/.config" > "$log/SHA256SUMS"
strings "$log/Image" | grep -Fx 'wlan/qca_cld/qca6390/WCNSS_qcom_cfg.ini'
strings "$log/Image" | grep -Fx 'wlan/qca_cld/qca6390/wlan_mac.bin'
echo 'R107_EROFS_QCA6390_IMAGE_BUILT'
