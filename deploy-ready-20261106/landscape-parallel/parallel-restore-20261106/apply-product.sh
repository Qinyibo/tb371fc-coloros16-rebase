#!/system/bin/sh
set -e
FO_SRC=/data/local/tmp/sys_full_orientation_managed.parallel-v1.xml
FW_SRC=/data/local/tmp/sys_fantasy_window_managed.parallel-v1.xml
FO_TARGET=/my_product/etc/fantasy/sys_full_orientation_managed.xml
FW_TARGET=/my_product/etc/fantasy/sys_fantasy_window_managed.xml
STAMP=$(date +%Y%m%d-%H%M%S)
id | grep -q uid=0 || { echo FAIL need root; exit 1; }
[ -f "$FO_SRC" ] && [ -f "$FW_SRC" ] || { echo FAIL missing src; exit 2; }
FO_PRE=$(md5sum "$FO_TARGET" | awk '{print $1}')
FW_PRE=$(md5sum "$FW_TARGET" | awk '{print $1}')
echo FO_PRE=$FO_PRE
echo FW_PRE=$FW_PRE
cp -f "$FO_TARGET" /data/local/tmp/sys_fo.pre-parallel-$STAMP.xml
cp -f "$FW_TARGET" /data/local/tmp/sys_fw.pre-parallel-$STAMP.xml
mount -o remount,rw / || { echo FAIL remount; exit 3; }
cp -f "$FO_SRC" "$FO_TARGET"
cp -f "$FW_SRC" "$FW_TARGET"
chmod 644 "$FO_TARGET" "$FW_TARGET"
chown root:root "$FO_TARGET" "$FW_TARGET"
restorecon "$FO_TARGET" 2>/dev/null || true
restorecon "$FW_TARGET" 2>/dev/null || true
sync
FO_POST=$(md5sum "$FO_TARGET" | awk '{print $1}')
FW_POST=$(md5sum "$FW_TARGET" | awk '{print $1}')
echo FO_POST=$FO_POST
echo FW_POST=$FW_POST
EXPECT_FO=$(md5sum "$FO_SRC" | awk '{print $1}')
EXPECT_FW=$(md5sum "$FW_SRC" | awk '{print $1}')
[ "$FO_POST" = "$EXPECT_FO" ] || { echo FAIL FO md5; mount -o remount,ro / 2>/dev/null || true; exit 4; }
[ "$FW_POST" = "$EXPECT_FW" ] || { echo FAIL FW md5; mount -o remount,ro / 2>/dev/null || true; exit 5; }
grep -o 'package_name="com.tencent.mm" status="[0-9]"' "$FO_TARGET" | head -1
grep -o 'package_name="com.tencent.mm" status="[0-9]"' "$FW_TARGET" | head -1
grep -o 'package_name="com.tencent.mobileqq" status="[0-9]"' "$FW_TARGET" | head -1
grep -o 'package_name="com.ss.android.ugc.aweme" status="[0-9]"' "$FW_TARGET" | head -1
mount -o remount,ro / 2>/dev/null || echo WARN remount ro
echo OK_PRODUCT_PARALLEL