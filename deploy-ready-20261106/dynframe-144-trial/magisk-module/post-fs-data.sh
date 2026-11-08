#!/system/bin/sh
MODDIR=${0%/*}
TARGET=/my_product/etc/sys_dynamic_frame_config.xml
SRC=$MODDIR/my_product/etc/sys_dynamic_frame_config.xml
if [ -f "$SRC" ]; then
  mount --bind "$SRC" "$TARGET"
fi
