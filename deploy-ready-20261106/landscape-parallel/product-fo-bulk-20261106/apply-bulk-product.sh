#!/system/bin/sh
set -e
FO_SRC=/data/local/tmp/sys_full_orientation_managed.bulk-v1.xml
FW_SRC=/data/local/tmp/sys_fantasy_window_managed.bulk-v1.xml
FO_TARGET=/my_product/etc/fantasy/sys_full_orientation_managed.xml
FW_TARGET=/my_product/etc/fantasy/sys_fantasy_window_managed.xml
STAMP=$(date +%Y%m%d-%H%M%S)
FO_BAK=/data/local/tmp/sys_full_orientation_managed.pre-bulk-$STAMP.xml
FW_BAK=/data/local/tmp/sys_fantasy_window_managed.pre-bulk-$STAMP.xml
EXPECT_FO_PRE1=5848af15cce834a875202d32953be164
EXPECT_FO_PRE2=1986e9bec618ed4ea2eaee78fff9e5ce
EXPECT_FO_POST=1986e9bec618ed4ea2eaee78fff9e5ce
EXPECT_FW_POST=$(md5sum "$FW_SRC" | awk '{print $1}')

id | grep -q uid=0 || { echo FAIL need root; exit 1; }
[ -f "$FO_SRC" ] || { echo FAIL missing FO src; exit 2; }
[ -f "$FW_SRC" ] || { echo FAIL missing FW src; exit 2; }

FO_PRE=$(md5sum "$FO_TARGET" | awk '{print $1}')
FW_PRE=$(md5sum "$FW_TARGET" | awk '{print $1}')
echo FO_PRE=$FO_PRE
echo FW_PRE=$FW_PRE
case "$FO_PRE" in
  $EXPECT_FO_PRE1|$EXPECT_FO_PRE2) ;;
  *) echo FAIL unexpected FO pre md5; exit 3 ;;
esac

cp -f "$FO_TARGET" "$FO_BAK"
cp -f "$FW_TARGET" "$FW_BAK"
chmod 644 "$FO_BAK" "$FW_BAK"

mount -o remount,rw / || { echo FAIL remount rw; exit 4; }
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
[ "$FO_POST" = "$EXPECT_FO_POST" ] || { echo FAIL FO md5; mount -o remount,ro / 2>/dev/null || true; exit 5; }
[ "$FW_POST" = "$EXPECT_FW_POST" ] || { echo FAIL FW md5; mount -o remount,ro / 2>/dev/null || true; exit 6; }

# spot checks
grep -o 'package_name="com.tencent.mm" status="[0-9]"' "$FO_TARGET" | head -1
grep -o 'package_name="com.tencent.mobileqq" status="[0-9]"' "$FO_TARGET" | head -1
grep -o 'package_name="com.ss.android.ugc.aweme" status="[0-9]"' "$FO_TARGET" | head -1
grep -c 'package_name="com.heytap.yoli"' "$FO_TARGET"
grep -c 'package_name="com.heytap.yoli"' "$FW_TARGET"

mount -o remount,ro / 2>/dev/null || echo WARN remount ro
echo FO_BAK=$FO_BAK
echo FW_BAK=$FW_BAK
echo OK_PRODUCT_BULK_BAKE
