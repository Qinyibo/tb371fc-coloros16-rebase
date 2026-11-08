#!/system/bin/sh
MODDIR=${0%/*}
TARGET=/my_product/etc/oplus_vrr_config.json
SRC="$MODDIR/oplus_vrr_config.json"
[ -f "$SRC" ] && [ -f "$TARGET" ] || exit 0
mount -o bind "$SRC" "$TARGET"
