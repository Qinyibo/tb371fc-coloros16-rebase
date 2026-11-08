@echo off
setlocal
set PROBE=%~dp0probe
adb push "%PROBE%\fantasywindow.db.bak" /sdcard/Download/fantasywindow.db.bak
adb push "%PROBE%\rollback-native.sh" /sdcard/Download/rollback-native.sh
adb shell su -c "sh /sdcard/Download/rollback-native.sh"
echo Done. am force-stop com.ss.android.ugc.aweme then relaunch.
