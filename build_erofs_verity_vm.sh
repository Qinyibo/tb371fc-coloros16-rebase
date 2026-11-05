#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
dst=/work/tb371fc-clean-rebase-r107-erofs-20261104
src="$dst/src"; out="$dst/vm-out"
log="$r/erofs-kernel-vm"
export PATH=/usr/lib/llvm-21/bin:$PATH LD_LIBRARY_PATH=/root/tc-shim/lib TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
mkdir -p "$out" "$log"
old=/work/tb371fc-erofs-minimal-vm-20261001/config.final
cp "$old" "$out/.config"
"$src/scripts/config" --file "$out/.config" -d HYBRIDMOUNT -d GOODIX_FINGERPRINT -e SECURITY -e SECURITY_NETWORK -e AUDIT -e SECURITY_SELINUX -e KEYS -e EXT4_FS -e FS_ENCRYPTION -e FS_VERITY -e CRYPTO_LIB_BLAKE2S -e COMPAT -e MD -e MISC_FILESYSTEMS -e BLK_DEV_DM -e DM_VERITY -e CRYPTO_SHA256 -e EROFS_FS -e EROFS_FS_XATTR -e EROFS_FS_SECURITY -e EROFS_FS_ZIP
export KBUILD_BUILD_USER=tb371fc-offline KBUILD_BUILD_HOST=r107-erofs-virt KBUILD_BUILD_TIMESTAMP='Sat Oct 31 2026 20:00:00 +0800' KBUILD_BUILD_VERSION=1
flags='-Wno-error -Wno-error=strict-prototypes -Wno-error=implicit-int -Wno-error=incompatible-pointer-types -Wno-error=date-time'
make_k() { make -C "$src" O="$out" ARCH=arm64 CC=clang CLANG_TRIPLE=aarch64-linux-gnu- CROSS_COMPILE=aarch64-linux-gnu- AS=aarch64-linux-gnu-as LOCALVERSION= "$@"; }
make_k olddefconfig > "$log/config.log" 2>&1
grep -E '^(CONFIG_DM_VERITY|CONFIG_BLK_DEV_DM|CONFIG_EROFS_FS|CONFIG_CRYPTO_SHA256)=y$' "$out/.config" | sort > "$log/active.txt"
test "$(wc -l < "$log/active.txt")" = 4
make_k -j6 KCFLAGS="$flags" Image > "$log/build.log" 2>&1
cp "$out/arch/arm64/boot/Image" "$out/.config" "$log/"
echo 'R107_EROFS_QEMU_DM_VERITY_IMAGE_BUILT'
