#!/system/bin/sh
set -e
FW_SRC=/data/local/tmp/sys_fantasy_window_managed.qq-fix.xml
FW_TARGET=/my_product/etc/fantasy/sys_fantasy_window_managed.xml
STAMP=$(date +%Y%m%d-%H%M%S)
FW_BAK=/data/local/tmp/sys_fantasy_window_managed.pre-qqfix-$STAMP.xml
id | grep -q uid=0 || { echo FAIL need root; exit 1; }
[ -f "$FW_SRC" ] || { echo FAIL missing FW src; exit 2; }
FW_PRE=$(md5sum "$FW_TARGET" | awk '{print $1}')
echo FW_PRE=$FW_PRE
cp -f "$FW_TARGET" "$FW_BAK"
chmod 644 "$FW_BAK"
mount -o remount,rw / || { echo FAIL remount rw; exit 4; }
cp -f "$FW_SRC" "$FW_TARGET"
chmod 644 "$FW_TARGET"
chown root:root "$FW_TARGET"
restorecon "$FW_TARGET" 2>/dev/null || true
sync
FW_POST=$(md5sum "$FW_TARGET" | awk '{print $1}')
echo FW_POST=$FW_POST
EXPECT=$(md5sum "$FW_SRC" | awk '{print $1}')
[ "$FW_POST" = "$EXPECT" ] || { echo FAIL FW md5; mount -o remount,ro / 2>/dev/null || true; exit 6; }
grep -o 'package_name="com.tencent.mobileqq"[^/]*/>' "$FW_TARGET" | head -c 400; echo
grep -c 'SplashActivity' "$FW_TARGET"
mount -o remount,ro / 2>/dev/null || echo WARN remount ro
echo FW_BAK=$FW_BAK
echo OK_PRODUCT_QQ_FIX