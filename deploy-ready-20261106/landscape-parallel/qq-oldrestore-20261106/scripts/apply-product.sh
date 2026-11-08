#!/system/bin/sh
set -e
FW_SRC=/data/local/tmp/sys_fantasy_window_managed.oldrestore.xml
FO_SRC=/data/local/tmp/sys_full_orientation_managed.oldrestore.xml
FW_TARGET=/my_product/etc/fantasy/sys_fantasy_window_managed.xml
FO_TARGET=/my_product/etc/fantasy/sys_full_orientation_managed.xml
STAMP=$(date +%Y%m%d-%H%M%S)
cp -f "$FW_TARGET" /data/local/tmp/sys_fantasy_window_managed.pre-oldrestore-$STAMP.xml
cp -f "$FO_TARGET" /data/local/tmp/sys_full_orientation_managed.pre-oldrestore-$STAMP.xml
mount -o remount,rw /
cp -f "$FW_SRC" "$FW_TARGET"
cp -f "$FO_SRC" "$FO_TARGET"
chmod 644 "$FW_TARGET" "$FO_TARGET"
chown root:root "$FW_TARGET" "$FO_TARGET"
restorecon "$FW_TARGET" "$FO_TARGET" 2>/dev/null || true
sync
echo FW=$(md5sum "$FW_TARGET" | awk '{print $1}')
echo FO=$(md5sum "$FO_TARGET" | awk '{print $1}')
grep -o 'package_name="com.tencent.mobileqq"[^/]*/>' "$FW_TARGET" | head -c 280; echo
grep -o 'package_name="com.tencent.mobileqq"[^/]*/>' "$FO_TARGET"; echo
mount -o remount,ro / 2>/dev/null || true
echo OK_PRODUCT_OLDRESTORE