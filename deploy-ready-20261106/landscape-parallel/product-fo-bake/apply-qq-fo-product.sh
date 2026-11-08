#!/system/bin/sh
set -e
SRC=/data/local/tmp/sys_full_orientation_managed.qq-fo-v1.xml
TARGET=/my_product/etc/fantasy/sys_full_orientation_managed.xml
BAK=/data/local/tmp/sys_full_orientation_managed.pre-qqfo-$(date +%Y%m%d-%H%M%S).xml
EXPECT_STOCK=7aef2aef34f93761e37ec01fc589d533
EXPECT_BAKE=5848af15cce834a875202d32953be164
id | grep -q uid=0 || { echo FAIL need root; exit 1; }
PRE=$(md5sum "$TARGET" | awk '{print $1}')
echo PRE=$PRE
[ "$PRE" = "$EXPECT_STOCK" ] || [ "$PRE" = "$EXPECT_BAKE" ] || { echo FAIL unexpected pre md5; exit 2; }
cp -f "$TARGET" "$BAK"
chmod 644 "$BAK"
mount -o remount,rw / || { echo FAIL remount rw; exit 3; }
cp -f "$SRC" "$TARGET"
chmod 644 "$TARGET"
chown root:root "$TARGET"
restorecon "$TARGET" 2>/dev/null || true
sync
POST=$(md5sum "$TARGET" | awk '{print $1}')
echo POST=$POST
grep -o 'package_name="com.tencent.mobileqq" status="[0-9]"' "$TARGET"
grep -o 'package_name="com.ss.android.ugc.aweme" status="[0-9]"' "$TARGET"
[ "$POST" = "$EXPECT_BAKE" ] || { echo FAIL md5; mount -o remount,ro / 2>/dev/null || true; exit 4; }
mount -o remount,ro / 2>/dev/null || echo WARN remount ro
echo BAK=$BAK
echo OK_PRODUCT_FO_BAKE
