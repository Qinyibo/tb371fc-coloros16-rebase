#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
out="$r/boot-cleanbase"
test ! -e "$out"
mkdir -p "$out/work" "$out/readback"
cp "$r/boot-audit/magiskboot" "$out/magiskboot"
chmod 755 "$out/magiskboot"
cd "$out/work"
../magiskboot unpack "$r/tb-inputs/boot-r107.img" > "$out/unpack.log" 2>&1
# Remove only the former project bootstrap and its private assets. Magisk's
# own init/backup/core assets, the TB fstab, kernel and DTB remain unchanged.
../magiskboot cpio ramdisk.cpio \
 'rm overlay.d/r93-init.rc' \
 'rm overlay.d/sbin/r91-SHA256SUMS' \
 'rm overlay.d/sbin/r91-apply.sh' \
 'rm overlay.d/sbin/r93-apply.sh' \
 'rm overlay.d/sbin/r93-health.sh' \
 'rm overlay.d/sbin/r93-magisk-bin.tgz' \
 'rm overlay.d/sbin/r93-manager.apk' \
 'rm overlay.d/sbin/r93-manager.sh' \
 'rm overlay.d/sbin/r93-seed-base.sh' \
 'rm overlay.d/sbin/r93-seed.sh' > "$out/cpio-change.log" 2>&1
../magiskboot repack "$r/tb-inputs/boot-r107.img" "$out/boot-r107-cleanbase.img" > "$out/repack.log" 2>&1
cd "$out/readback"
../magiskboot unpack "$out/boot-r107-cleanbase.img" > "$out/readback.log" 2>&1
cmp kernel "$r/boot-audit/kernel"
cmp dtb "$r/boot-audit/dtb"
test "$(stat -c%s "$out/boot-r107-cleanbase.img")" = 100663296
sha256sum "$out/boot-r107-cleanbase.img" > "$out/SHA256SUMS"
echo CLEAN_BOOT_REPACK_KERNEL_DTB_PRESERVED
