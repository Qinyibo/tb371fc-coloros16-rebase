#!/usr/bin/env bash
# REQUIRES explicit operator approval.
# Usage:
#   ./flash-install.sh            # dry-run hash check
#   ./flash-install.sh flash      # flash Magisk boot + reboot ONLY
#   ./flash-install.sh module     # install module + reboot + verify
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PATCHED="$ROOT/boot-r108-resx-magisk.img"
STOCK="E:/youxikaifa/work/today-20261109/boot-r108-resx.img"
ZIP="$ROOT/tb371fc_tinno_vintf_pair.zip"
EXPECT_PATCHED="62428f25f857bcc15fe8ab4a3a18148c5b37723109de60f974c470188839a825"
EXPECT_STOCK="f5f446047721e788451fbde8d984a8e3dca0ac21e18e85f9f15839c6289b1f13"
EXPECT_ZIP="16e3f4ff045d824482efcd5ce92251129a8fcb2326f38bc36978ad6cf3ab2078"

sha_of() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print tolower($1)}'
  else
    certutil -hashfile "$1" SHA256 | awk 'NR==2{print tolower($0)}'
  fi
}
check() {
  local g; g=$(sha_of "$1")
  if [[ "$g" != "$2" ]]; then echo "SHA mismatch $1 got=$g expect=$2"; exit 1; fi
  echo "OK $1"
}
check "$PATCHED" "$EXPECT_PATCHED"
check "$STOCK" "$EXPECT_STOCK"
check "$ZIP" "$EXPECT_ZIP"

cmd="${1:-dry}"
if [[ "$cmd" == "dry" ]]; then
  echo "DRY RUN OK. Pass flash or module explicitly."
  exit 0
fi
if [[ "$cmd" == "flash" ]]; then
  adb reboot bootloader
  sleep 8
  fastboot devices
  fastboot flash boot_a "$PATCHED"
  fastboot set_active a
  fastboot reboot
  adb wait-for-device
  echo "Magisk boot flashed. Then: $0 module"
  exit 0
fi
if [[ "$cmd" == "module" ]]; then
  adb push "$ZIP" /data/local/tmp/tb371fc_tinno_vintf_pair.zip
  adb shell su -c 'magisk --install-module /data/local/tmp/tb371fc_tinno_vintf_pair.zip'
  adb reboot
  adb wait-for-device
  for i in $(seq 1 60); do
    bc=$(adb shell getprop sys.boot_completed | tr -d '\r')
    [[ "$bc" == "1" ]] && break
    sleep 3
  done
  adb shell getprop init.svc.tinnokeyboard
  adb shell getprop ro.build.display.id
  adb shell su -c 'grep -n tinno /vendor/etc/vintf/compatibility_matrix.xml'
  adb shell su -c 'ls -l /vendor/etc/vintf/manifest/*tinno* 2>/dev/null; ls -l /data/adb/modules/tb371fc_tinno_vintf_pair'
  exit 0
fi
echo "unknown cmd: $cmd"; exit 2