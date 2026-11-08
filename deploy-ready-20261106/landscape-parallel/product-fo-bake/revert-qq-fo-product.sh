#!/system/bin/sh
set -e
SRC=/data/local/tmp/sys_full_orientation_managed.stock.xml
TARGET=/my_product/etc/fantasy/sys_full_orientation_managed.xml
EXPECT=7aef2aef34f93761e37ec01fc589d533
id | grep -q uid=0 || exit 1
mount -o remount,rw /
cp -f "$SRC" "$TARGET"
chmod 644 "$TARGET"
chown root:root "$TARGET"
restorecon "$TARGET" 2>/dev/null || true
sync
POST=$(md5sum "$TARGET" | awk '{print $1}')
echo POST=$POST
[ "$POST" = "$EXPECT" ] || { echo FAIL md5; exit 2; }
mount -o remount,ro / 2>/dev/null || true
echo OK_REVERT_PRODUCT_FO
