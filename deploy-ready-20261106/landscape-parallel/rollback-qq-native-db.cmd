@echo off
set PROBE=%~dp0probe
adb push "%PROBE%\fantasywindow.before-qq-fo-20261106.db" /sdcard/Download/fantasywindow.before-qq-fo-20261106.db
adb shell su -c "PID=$(pidof com.oplus.exsystemservice); su -t $PID -c 'cp -f /sdcard/Download/fantasywindow.before-qq-fo-20261106.db /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'; su -t $PID -c 'chmod 660 /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'; kill -9 $PID"
adb shell am force-stop com.tencent.mobileqq
echo Rolled back INTERIM DB only. Product FO bake still present unless reverted separately.
