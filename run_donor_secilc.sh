#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
out="$r/integrated-logicals"
d=/work/tb371fc-clean-rebase-policy-android16-20261104
mkdir "$d" "$out/donor-policy"
mkdir -p "$d"/{sroot,system,system_ext,product,vendor,odm,apex/com.android.runtime,dev,output}
mount -t ext4 -o loop,ro "$out/system.img" "$d/sroot"
mount --bind "$d/sroot/system" "$d/system"
for p in system_ext product; do mount -t ext4 -o loop,ro "$out/$p.img" "$d/$p"; done
for p in vendor odm; do mount --bind "$r/mounts/tb-$p" "$d/$p"; mount -o remount,bind,ro "$d/$p"; done
mount --bind "$r/mounts/com.android.runtime" "$d/apex/com.android.runtime"
mount --bind "$out/donor-policy" "$d/output"
cp /usr/bin/qemu-aarch64-static "$d/qemu-aarch64-static"
version="$(cat "$d/vendor/etc/selinux/plat_sepolicy_vers.txt")"
test "$version" = 30.0
s=/system/etc/selinux; x=/system_ext/etc/selinux; y=/product/etc/selinux; v=/vendor/etc/selinux; o=/odm/etc/selinux
cil=("$s/plat_sepolicy.cil" "$s/mapping/$version.cil")
for f in "$s/mapping/$version.compat.cil" "$x/system_ext_sepolicy.cil" "$x/mapping/$version.cil" "$x/mapping/$version.compat.cil"  "$y/product_sepolicy.cil" "$y/mapping/$version.cil" "$v/plat_pub_versioned.cil" "$v/vendor_sepolicy.cil" "$o/odm_sepolicy.cil"; do
 if test -f "$d/$f"; then cil+=("$f"); fi
done
chroot "$d" /qemu-aarch64-static -E LD_LIBRARY_PATH=/system/lib64:/apex/com.android.runtime/lib64/bionic /system/bin/secilc "${cil[0]}" -m -M true -G -N -c 30 "${cil[@]:1}" -o /output/runtime-sepolicy -f /output/runtime-file_contexts > "$out/donor-policy/compile.log" 2>&1
sha256sum "$out/donor-policy/runtime-sepolicy" "$out/runtime-sepolicy" | tee "$out/donor-policy/SHA256SUMS"
if cmp -s "$out/donor-policy/runtime-sepolicy" "$out/runtime-sepolicy"; then echo DONOR_SEPOLICY_BYTE_IDENTICAL; else echo DONOR_SEPOLICY_DISTINCT_NEEDS_KERNEL_LOAD; fi
