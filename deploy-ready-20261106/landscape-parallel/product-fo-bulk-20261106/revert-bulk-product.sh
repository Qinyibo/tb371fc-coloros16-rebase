#!/system/bin/sh
set -e
FO_SRC=/data/local/tmp/sys_full_orientation_managed.pre-bulk.xml
FW_SRC=/data/local/tmp/sys_fantasy_window_managed.pre-bulk.xml
FO_TARGET=/my_product/etc/fantasy/sys_full_orientation_managed.xml
FW_TARGET=/my_product/etc/fantasy/sys_fantasy_window_managed.xml
id | grep -q uid=0 || { echo FAIL need root; exit 1; }
[ -f "$FO_SRC" ] || { echo FAIL missing FO revert src; exit 2; }
[ -f "$FW_SRC" ] || { echo FAIL missing FW revert src; exit 2; }
mount -o remount,rw / || { echo FAIL remount rw; exit 3; }
cp -f "$FO_SRC" "$FO_TARGET"
cp -f "$FW_SRC" "$FW_TARGET"
chmod 644 "$FO_TARGET" "$FW_TARGET"
chown root:root "$FO_TARGET" "$FW_TARGET"
sync
echo FO_POST=$(md5sum "$FO_TARGET" | awk '{print $1}')
echo FW_POST=$(md5sum "$FW_TARGET" | awk '{print $1}')
mount -o remount,ro / 2>/dev/null || echo WARN remount ro
echo OK_PRODUCT_BULK_REVERT
