#!/system/bin/sh
MODDIR=${0%/*}
TARGET=/system/framework/oplus-services.jar
SRC="$MODDIR/system/framework/oplus-services.jar"
[ -f "$SRC" ] || exit 0
mount -o bind "$SRC" "$TARGET"