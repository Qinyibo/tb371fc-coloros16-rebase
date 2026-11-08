#!/system/bin/sh
set -e
SRC=/data/local/tmp/refresh_rate_config.B1-type2.xml
TARGET=/my_product/etc/refresh_rate_config.xml
BAK=/data/local/tmp/refresh_rate_config.pre-keepB1-$(date +%Y%m%d-%H%M%S).xml
id | grep -q uid=0 || exit 1
PRE=$(md5sum "$TARGET" | awk '{print $1}')
echo PRE=$PRE
cp -f "$TARGET" "$BAK"
mount -o remount,rw /
cp -f "$SRC" "$TARGET"
chmod 644 "$TARGET"
chown root:root "$TARGET"
restorecon "$TARGET" 2>/dev/null || true
sync
POST=$(md5sum "$TARGET" | awk '{print $1}')
echo POST=$POST
grep -o 'appSwitchBoostType="[0-9]"' "$TARGET"
mount -o remount,ro / 2>/dev/null || true
echo OK_KEEP