#!/system/bin/sh
set -e
SRC=/data/local/tmp/refresh_rate_config.pre-B1.xml
TARGET=/my_product/etc/refresh_rate_config.xml
EXPECT=35db38f8c85758c372546c707513642c
id | grep -q uid=0 || exit 1
mount -o remount,rw /
cp -f "$SRC" "$TARGET"
chmod 644 "$TARGET"
chown root:root "$TARGET"
restorecon "$TARGET" 2>/dev/null || true
sync
POST=$(md5sum "$TARGET" | awk '{print $1}')
echo POST=$POST
grep -o 'appSwitchBoostType="[0-9]"' "$TARGET"
[ "$POST" = "$EXPECT" ] || { echo FAIL md5; exit 2; }
mount -o remount,ro / 2>/dev/null || true
echo OK_REVERT