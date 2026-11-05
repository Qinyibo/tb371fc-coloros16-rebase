#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
sha256sum "$r/mounts/system_ext/priv-app/OplusLauncher/OplusLauncher.apk" "$r/mounts/tb-vendor/firmware/tfa98xx_QS.cnt"
grep -nE 'ro.sf.lcd_density|oplus.anim|animationlevel' "$r/mounts/my_product/build.prop" "$r/mounts/my_manifest/build.prop" || true
ls "$r/mounts/tb-vendor/bin" | grep -E 'mixer|tiny'
grep -nE 'Swap channel|Rotation|rotation' "$r/mounts/tb-vendor/etc/mixer_paths.xml" | head -30 || true
