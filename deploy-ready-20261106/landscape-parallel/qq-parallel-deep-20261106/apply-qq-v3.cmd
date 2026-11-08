@echo off
set ADB=C:\android-sdk\platform-tools\adb.exe
%ADB% wait-for-device
%ADB% push "%~dp0payload\sys_fantasy_window_managed.qq-v3.xml" /data/local/tmp/sys_fantasy_window_managed.qq-v3.xml
%ADB% push "%~dp0payload\fantasywindow.qq-v3.db" /sdcard/Download/fantasywindow.qq-v3.db
%ADB% push "%~dp0scripts\apply-product-v3.sh" /data/local/tmp/apply-qq-v3-product.sh
%ADB% push "%~dp0scripts\apply-db-v3.sh" /data/local/tmp/apply-qq-v3-db.sh
%ADB% shell su -c "chmod 755 /data/local/tmp/apply-qq-v3-product.sh /data/local/tmp/apply-qq-v3-db.sh; /data/local/tmp/apply-qq-v3-product.sh; /data/local/tmp/apply-qq-v3-db.sh"
%ADB% shell am force-stop com.tencent.mobileqq
echo OK apply v3
