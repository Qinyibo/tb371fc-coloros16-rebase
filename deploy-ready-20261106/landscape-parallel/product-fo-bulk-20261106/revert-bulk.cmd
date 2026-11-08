@echo off
set HERE=%~dp0
adb push "%HERE%sys_full_orientation_managed.pre-bulk.xml" /data/local/tmp/sys_full_orientation_managed.pre-bulk.xml
adb push "%HERE%sys_fantasy_window_managed.pre-bulk.xml" /data/local/tmp/sys_fantasy_window_managed.pre-bulk.xml
adb push "%HERE%revert-bulk-product.sh" /data/local/tmp/revert-bulk-product.sh
adb shell su -mm -c "sh /data/local/tmp/revert-bulk-product.sh"
echo Reverted product FO/fantasy XMLs to pre-bulk. Restore DB via prior fw-bulk.db if needed.
