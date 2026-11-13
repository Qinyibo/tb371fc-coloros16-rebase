#!/bin/bash
# Run on Qin (Windows) once connected: via Git Bash or WSL TB371FC-Builder + adb/fastboot on PATH.
# Preferred path: pack on-device with Magisk's magiskboot, flash Magisk boot_a only.
set -euo pipefail
DIAG='E:/youxikaifa/work/today-20261109/boot-diag'
IMG="$DIAG/force-rek-Image"
BASE_MAGISK='E:/youxikaifa/work/today-20261109/kb-vintf-magisk/boot-r108-resx-magisk.img'
BASE_STOCK="$DIAG/force-rek-base-r108.img"
OUT_MAGISK="$DIAG/boot-r108-force-rek-magisk.img"
OUT_STOCK="$DIAG/boot-r108-force-rek.img"

adb wait-for-device
adb push "$IMG" /data/local/tmp/force-rek-Image
adb push "$BASE_MAGISK" /data/local/tmp/magisk-base.img
adb push "$BASE_STOCK" /data/local/tmp/stock-base.img
adb shell su -c '
set -e
MB=/data/adb/magisk/magiskboot
cd /data/local/tmp
rm -rf frk && mkdir frk && cd frk
cp ../magisk-base.img .
$MB unpack magisk-base.img
cp ../force-rek-Image kernel
$MB repack magisk-base.img boot-r108-force-rek-magisk.img
cp ../stock-base.img .
$MB unpack stock-base.img
cp ../force-rek-Image kernel
$MB repack stock-base.img boot-r108-force-rek.img
sha256sum boot-r108-force-rek-magisk.img boot-r108-force-rek.img
'
adb pull /data/local/tmp/frk/boot-r108-force-rek-magisk.img "$OUT_MAGISK"
adb pull /data/local/tmp/frk/boot-r108-force-rek.img "$OUT_STOCK"
echo "Packed. Reboot to fastboot and flash Magisk boot_a only..."
adb reboot bootloader
fastboot flash boot_a "$OUT_MAGISK"
fastboot reboot
# then wait boot_completed, sleep/wake, collect R10x_FORCE_REK dmesg
