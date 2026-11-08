@echo off
set HERE=%~dp0
echo Restore fantasy XML from /data/local/tmp/sys_fantasy_window_managed.pre-qqfix-*.xml manually if needed
adb push "%HERE%fantasywindow.pre.db" /sdcard/Download/fantasywindow.qq-revert.db
adb shell su -c "PID=$(pidof com.oplus.exsystemservice); su -t $PID -c 'cp -f /sdcard/Download/fantasywindow.qq-revert.db /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'; su -t $PID -c 'chmod 660 /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'; su -t $PID -c 'chown system:system /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'; kill -9 $PID"
adb shell am force-stop com.tencent.mobileqq
echo Reverted DB to pre-qq-fix
