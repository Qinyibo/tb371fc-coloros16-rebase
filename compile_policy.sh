#!/bin/bash
set -eu
r=/mnt/d/TB371FC-release/clean-rebase-20261104
out="$r/policy-check"
mkdir -p "$out"
plat="$r/mounts/system/system/etc/selinux"
ext="$r/mounts/system_ext/etc/selinux"
product="$r/mounts/product/etc/selinux"
vendor="$r/tb-readback/selinux-vendor/selinux"
set -- "$plat/plat_sepolicy.cil" "$plat/mapping/30.0.cil"
for p in "$plat/mapping/30.0.compat.cil" "$ext/system_ext_sepolicy.cil" "$ext/mapping/30.0.cil" "$product/product_sepolicy.cil" "$product/mapping/30.0.cil" "$vendor/plat_pub_versioned.cil" "$vendor/vendor_sepolicy.cil"; do
 if test -f "$p"; then set -- "$@" "$p"; fi
done
if test -f "$out/legacy-vendor-types.cil"; then set -- "$@" "$out/legacy-vendor-types.cil"; fi
sha256sum "$@" > "$out/input-SHA256SUMS"
secilc --version > "$out/compiler-version.txt" 2>&1 || true
# The strict check is supplementary. Android 16 init itself uses -N when
# combining separately built legacy vendor policy with platform policy; see
# the pinned AOSP source saved beside this script. Keep both results distinct.
if test "${REBASE_POLICY_MODE:-strict}" = runtime; then
 secilc -m -M true -G -N -c 30 "$@" -o "$out/runtime-sepolicy" -f "$out/runtime-file_contexts" > "$out/runtime-compile.log" 2>&1
 echo STANDARD_INIT_POLICY_LINK_PASS
else
 secilc -m -M true -G -c 30 "$@" -o "$out/sepolicy" -f "$out/file_contexts" > "$out/compile.log" 2>&1
 echo STRICT_POLICY_CHECK_PASS
fi
