@echo off
set HERE=%~dp0
adb push "%HERE%sys_full_orientation_managed.stock.xml" /data/local/tmp/sys_full_orientation_managed.stock.xml
adb push "%HERE%revert-qq-fo-product.sh" /data/local/tmp/revert-qq-fo-product.sh
adb shell su -mm -c "sh /data/local/tmp/revert-qq-fo-product.sh"
