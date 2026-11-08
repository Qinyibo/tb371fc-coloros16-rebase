#!/system/bin/sh
set -e
SRC=/data/local/tmp/refresh_rate_config.B1-type2.xml
TARGET=/my_product/etc/refresh_rate_config.xml
BAK=/data/local/tmp/refresh_rate_config.pre-B1-$(date +%Y%m%d-%H%M%S).xml
EXPECT_B0=35db38f8c85758c372546c707513642c
id | grep -q uid=0 || { echo FAIL need root; exit 1; }
PRE=$(md5sum "$TARGET" | awk '{print $1}')
echo PRE=$PRE
[ "$PRE" = "$EXPECT_B0" ] || { echo FAIL unexpected pre md5; exit 2; }
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
grep -o 'appSwitchBoostType="[0-9]"' "$TARGET"
mount -o remount,ro / 2>/dev/null || echo WARN remount ro
echo BAK=$BAK
echo OK