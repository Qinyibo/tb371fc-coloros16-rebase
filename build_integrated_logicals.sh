#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
out="$r/integrated-logicals"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
mkdir "$out"
for n in system system_ext product; do mkdir "$out/mount-$n"; done
cleanup() {
 cd "$out"
 for n in system system_ext product; do if mountpoint -q "$out/mount-$n"; then umount "$out/mount-$n"; fi; done
}
trap cleanup EXIT
for n in system system_ext; do
 cp --reflink=auto --sparse=always "$r/base-ext4-UNADAPTED/$n.img" "$out/$n.img"
 if test "$n" = system_ext; then
  e2fsck -fp "$out/$n.img" > "$out/pre-grow-fsck.log" 2>&1
  truncate -s 1736441856 "$out/$n.img"
  resize2fs "$out/$n.img" > "$out/system-ext-grow.log" 2>&1
 fi
 mount -t ext4 -o rw,loop "$out/$n.img" "$out/mount-$n"
done
p="$out/mount-product"
truncate -s 25165824 "$out/product.img"
opts='^has_journal,^64bit,^metadata_csum,^flex_bg,^resize_inode,ext_attr,dir_index,filetype,extent,sparse_super,large_file,huge_file,uninit_bg,dir_nlink,extra_isize'
mke2fs -q -F -t ext4 -b 4096 -I 256 -L product -m 0 -N 1024 -O "$opts" "$out/product.img"
mount -t ext4 -o rw,loop "$out/product.img" "$p"
rsync -aHAX --numeric-ids "$r/mounts/product/" "$p/"
s="$out/mount-system"; e="$out/mount-system_ext"
cd "$s/system/framework"
echo '6d1280e25d0c40c12d1ed31877cfff40696d8d88cc089db5128cc2747c0bc7f2  oplus-services.jar' | sha256sum -c -
cat "$r/compat-framework/oplus-services.compat.jar" > oplus-services.jar
echo '25bbb67269b54965517d9d7fd9306dd0ba324f5ed89e7d7ad14960ab99e7c335  oplus-services.jar' | sha256sum -c -
for f in oplus-services.jar.fsv_meta oplus-services.jar.prof oplus-services.jar.prof.fsv_meta  oat/arm64/oplus-services.ocomp.art oat/arm64/oplus-services.ocomp.art.fsv_meta  oat/arm64/oplus-services.ocomp.odex oat/arm64/oplus-services.ocomp.odex.fsv_meta  oat/arm64/oplus-services.ocomp.vdex oat/arm64/oplus-services.ocomp.vdex.fsv_meta; do
 test -f "$f"
 rm -- "$f"
done
# Reuse the VNDK APEX used with TB vendor in v27. Match the existing APEX's
# placement context, mode and ownership while keeping the package bytes exact.
p="$e/apex/com.android.vndk.v30.apex"
test ! -e "$p"
cp -a "$e/apex/com.android.compos.apex" "$p"
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
