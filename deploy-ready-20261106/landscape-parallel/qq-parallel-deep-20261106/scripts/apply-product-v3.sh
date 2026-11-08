#!/system/bin/sh
set -e
FW_SRC=/data/local/tmp/sys_fantasy_window_managed.qq-v3.xml
FW_TARGET=/my_product/etc/fantasy/sys_fantasy_window_managed.xml
STAMP=$(date +%Y%m%d-%H%M%S)
FW_BAK=/data/local/tmp/sys_fantasy_window_managed.pre-qqv3-$STAMP.xml
cp -f "$FW_TARGET" "$FW_BAK"
mount -o remount,rw /
cp -f "$FW_SRC" "$FW_TARGET"
chmod 644 "$FW_TARGET"; chown root:root "$FW_TARGET"; restorecon "$FW_TARGET" 2>/dev/null || true
sync
echo FW_POST=$(md5sum "$FW_TARGET" | awk '{print $1}')
echo EXPECT=$(md5sum "$FW_SRC" | awk '{print $1}')
grep -o 'package_name="com.tencent.mobileqq"[^/]*/>' "$FW_TARGET" | head -c 350; echo
mount -o remount,ro / 2>/dev/null || true
echo FW_BAK=$FW_BAK
echo OK_PRODUCT_QQ_V3
