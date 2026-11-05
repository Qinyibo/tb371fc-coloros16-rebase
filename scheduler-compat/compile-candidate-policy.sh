#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/scheduler-compat/policy/candidate"
mkdir -p "$w"
export TMPDIR="$r/temp"
plat="$r/mounts/system/system/etc/selinux"
ext="$r/mounts/system_ext/etc/selinux"
product="$r/mounts/product/etc/selinux"
vendor="$r/tb-readback/selinux-vendor/selinux"
set -- "$plat/plat_sepolicy.cil" "$plat/mapping/30.0.cil"
for p in "$plat/mapping/30.0.compat.cil" "$r/scheduler-compat/policy/candidate-system_ext.cil" "$ext/mapping/30.0.cil" "$product/product_sepolicy.cil" "$product/mapping/30.0.cil" "$vendor/plat_pub_versioned.cil" "$vendor/vendor_sepolicy.cil"; do
 if test -f "$p"; then set -- "$@" "$p"; fi
done
sha256sum "$@" > "$w/input-SHA256SUMS"
secilc -m -M true -G -N -c 30 "$@" -o "$w/runtime-sepolicy" -f "$w/runtime-file_contexts" > "$w/runtime-compile.log" 2>&1
strict=0
secilc -m -M true -G -c 30 "$@" -o "$w/strict-sepolicy" -f "$w/strict-file_contexts" > "$w/strict-compile.log" 2>&1 || strict=$?
printf 'STANDARD_RUNTIME_POLICY_LINK_PASS strict_status=%s\n' "$strict"
