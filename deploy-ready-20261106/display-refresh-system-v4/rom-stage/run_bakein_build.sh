#!/usr/bin/env bash
set -euo pipefail
BASE=/mnt/d/TB371FC-release/clean-rebase-20261104
STAGE=$BASE/deploy-ready-20261106/display-refresh-system-v4/rom-stage
BAKEIN=$BASE/deploy-ready-20261106/display-refresh-system-v4/bake-in
DONOR_IMG=$BASE/donor-images/my_product.img
# Intermediate tree on Linux ext4 to preserve case collisions; final img only on D:
WORK=/home/ubuntu/work-bakein-20261106
PARTIAL_D=$STAGE/work-bakein-20261106
echo Cleaning partial D work and Linux WORK
rm -rf "$PARTIAL_D" "$WORK"
mkdir -p "$WORK" "$BAKEIN"
echo Extracting donor my_product.img to Linux WORK
fsck.erofs --extract="$WORK/my_product-bakein" --overwrite "$DONOR_IMG"
du -sh "$WORK/my_product-bakein"
echo Patching
python3 "$STAGE/patch_my_product_tree.py" "$WORK/my_product-bakein"
md5sum "$WORK/my_product-bakein/etc/refresh_rate_config.xml"
echo Building erofs to D bake-in folder
OUT="$BAKEIN/my_product-bakein.img"
rm -f "$OUT"
bash "$STAGE/rebuild_my_product_erofs.sh" "$WORK/my_product-bakein" "$OUT"
echo DONE
ls -la "$OUT"
sha256sum "$OUT"
md5sum "$OUT"
md5sum "$WORK/my_product-bakein/etc/refresh_rate_config.xml"
dump.erofs "$OUT" 2>&1 | head -20