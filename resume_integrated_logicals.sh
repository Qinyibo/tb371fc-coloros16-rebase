#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
out="$r/integrated-logicals"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
cd "$out"
cleanup() {
 cd "$out"
 for n in system system_ext product; do if mountpoint -q "$out/mount-$n"; then umount "$out/mount-$n"; fi; done
}
trap cleanup EXIT
test "$(stat -c%s system_ext.img)" = 1736441856
for n in system system_ext product; do
 mode=ro
 if test "$n" = system_ext; then mode=rw; fi
 mount -t ext4 -o "$mode,loop" "$out/$n.img" "$out/mount-$n"
done
s="$out/mount-system"; e="$out/mount-system_ext"
echo "25bbb67269b54965517d9d7fd9306dd0ba324f5ed89e7d7ad14960ab99e7c335  $s/system/framework/oplus-services.jar" | sha256sum -c -

p="$e/apex/com.android.vndk.v30.apex"
cat "$r/tb-readback/com.android.vndk.v30.apex" > "$p"
echo "f3c03c5cdfb8a1c1d92768dfc87d3526fa229fc4904a984da79ead97b3b7f6bd  $p" | sha256sum -c -
p="$e/etc/selinux"
orig="$(cat "$p/system_ext_sepolicy.cil" "$p/mapping/202504.cil" | sha256sum | cut -d' ' -f1)"
test "$orig" = "$(cat "$p/system_ext_sepolicy_and_mapping.sha256")"
printf '\n' >> "$p/system_ext_sepolicy.cil"
cat "$r/policy-check/legacy-vendor-types.cil" >> "$p/system_ext_sepolicy.cil"
cat "$p/system_ext_sepolicy.cil" "$p/mapping/202504.cil" | sha256sum | cut -d' ' -f1 > "$p/system_ext_sepolicy_and_mapping.sha256"
cd "$out"
version="$(cat "$r/mounts/tb-vendor/etc/selinux/plat_sepolicy_vers.txt")"; test "$version" = 30.0
p="$s/system/etc/selinux"; x="$e/etc/selinux"; y="$out/mount-product/etc/selinux"; v="$r/mounts/tb-vendor/etc/selinux"; o="$r/mounts/tb-odm/etc/selinux"
cil=("$p/plat_sepolicy.cil" "$p/mapping/$version.cil")
for f in "$p/mapping/$version.compat.cil" "$x/system_ext_sepolicy.cil" "$x/mapping/$version.cil" "$x/mapping/$version.compat.cil"  "$y/product_sepolicy.cil" "$y/mapping/$version.cil" "$v/plat_pub_versioned.cil" "$v/vendor_sepolicy.cil" "$o/odm_sepolicy.cil"; do
 if test -f "$f"; then cil+=("$f"); fi
done
test "$(cat "$p/plat_sepolicy_and_mapping.sha256")" != "$(cat "$o/precompiled_sepolicy.plat_sepolicy_and_mapping.sha256")"
sha256sum "${cil[@]}" > "$out/policy-input-sha256.txt"
secilc -m -M true -G -N -c 30 "${cil[@]}" -o "$out/runtime-sepolicy" -f "$out/runtime-file_contexts" > "$out/policy.log" 2>&1
sync -f "$s" "$e" "$out/mount-product"
cleanup
for n in system system_ext product; do e2fsck -fn "$out/$n.img" > "$out/fsck-$n.log" 2>&1; done
sha256sum "$out/"{system,system_ext,product}.img "$out/runtime-sepolicy" > "$out/SHA256SUMS"
echo INTEGRATED_LOGICALS_BUILT
