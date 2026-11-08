#!/system/bin/sh
MODDIR=${0%/*}
TARGET=/my_product/etc/refresh_rate_config.xml
SRC="$MODDIR/refresh_rate_config.xml"
[ -f "$SRC" ] || exit 0
[ -f "$TARGET" ] || exit 0
mount -o bind "$SRC" "$TARGET"