#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
d=/work/tb371fc-clean-rebase-vintf-20261104
mkdir -p "$d"
mkdir -p "$d"/{system,system_ext,product,vendor,odm,apex/com.android.runtime,apex/com.android.vndk.v30,dev,proc}
for p in system system_ext product vendor odm apex/com.android.runtime apex/com.android.vndk.v30; do
 case "$p" in system) from=system/system;; vendor|odm) from=tb-$p;; apex/*) from=${p#apex/};; *) from=$p;; esac
 mount --bind "$r/mounts/$from" "$d/$p"
 mount -o remount,bind,ro "$d/$p"
done
cp /usr/bin/qemu-aarch64-static "$d/qemu-aarch64-static"
mount --bind /dev/null "$d/dev/null" 2>/dev/null || { touch "$d/dev/null"; mount --bind /dev/null "$d/dev/null"; }
mount -t proc -o ro proc "$d/proc"
a="$d/system/lib64"
test -f "$a/libvintf.so"
chroot "$d" /qemu-aarch64-static -E LD_LIBRARY_PATH=/system/lib64:/apex/com.android.runtime/lib64/bionic /system/bin/vintf "$@"
