@echo off
REM rollback QQ magic to pre-v2 product XML bak if present, else v1 TIM splash body
adb wait-for-device
adb push "%~dp0payload\fantasywindow.pre-or-live-restore.note" /data/local/tmp/ 2>nul
echo Use device bak: /data/local/tmp/sys_fantasy_window_managed.pre-qqv2-*.xml OR pre-qqfix
echo Prefer: adb shell su -c "cp -f /data/local/tmp/sys_fantasy_window_managed.pre-qqv2-20261106-224648.xml /my_product/etc/fantasy/sys_fantasy_window_managed.xml"
echo Then restore DB from /sdcard/Download/fantasywindow.pre-qqv2.db or fantasywindow.pre-qqfix.db via su -t pidof exsystemservice
pause
