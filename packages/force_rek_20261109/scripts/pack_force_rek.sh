#!/bin/bash
set -euo pipefail
IMG=/work/r108-out/arch/arm64/boot/Image
echo '==== strings ===='
strings "$IMG" | grep R10x_FORCE_REK || true
strings "$IMG" | grep r108-force-rek || true
strings "$IMG" | grep R108_RESX_RELEASE || true
echo '==== pack stock boot ===='
WORKDIR=/work/r108-force-rek-pack
rm -rf "$WORKDIR"
mkdir -p "$WORKDIR"
cp /work/r108-pack/boot-r108-resx.img "$WORKDIR/base.img"
cp "$IMG" "$WORKDIR/kernel"
cp /work/r108-pack/dtb "$WORKDIR/dtb"
cp /work/r108-pack/ramdisk.cpio "$WORKDIR/ramdisk.cpio"
# Prefer magiskboot from Windows mount for unpack/repack of GKI boot
MAGISKBOOT=/mnt/e/youxikaifa/work/today-20261109/kb-vintf-magisk/magisk30.7-tools/magiskboot
if [ ! -x "$MAGISKBOOT" ]; then
  chmod +x "$MAGISKBOOT" || true
fi
cd "$WORKDIR"
cp base.img stock.img
"$MAGISKBOOT" unpack stock.img
ls -la
# replace kernel
cp /work/r108-out/arch/arm64/boot/Image kernel
"$MAGISKBOOT" repack stock.img boot-r108-force-rek.img
ls -la boot-r108-force-rek.img
sha256sum boot-r108-force-rek.img
cp boot-r108-force-rek.img /mnt/e/youxikaifa/work/today-20261109/boot-diag/
sha256sum /mnt/e/youxikaifa/work/today-20261109/boot-diag/boot-r108-force-rek.img
