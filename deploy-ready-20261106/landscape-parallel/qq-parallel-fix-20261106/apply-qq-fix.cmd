@echo off
set HERE=%~dp0
adb push "%HERE%payload\sys_fantasy_window_managed.qq-fix.xml" /data/local/tmp/sys_fantasy_window_managed.qq-fix.xml
adb push "%HERE%apply-product.sh" /data/local/tmp/apply-qq-product.sh
adb shell su -mm -c "sh /data/local/tmp/apply-qq-product.sh"
adb push "%HERE%payload\fantasywindow.qq-fix.db" /sdcard/Download/fantasywindow.qq-fix.db
adb push "%HERE%apply-db.sh" /sdcard/Download/apply-qq-db.sh
adb shell su -c "sh /sdcard/Download/apply-qq-db.sh"
adb shell am force-stop com.tencent.mobileqq
echo Done QQ parallel fix product+DB
