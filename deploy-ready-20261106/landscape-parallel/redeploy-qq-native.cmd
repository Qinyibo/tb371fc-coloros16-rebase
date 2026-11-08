@echo off
set PROBE=%~dp0probe
adb push "%PROBE%\fw-native-qq-v1.db" /sdcard/Download/fw-native-qq-v1.db
adb push "%PROBE%\deploy_qq_fo.sh" /sdcard/Download/deploy_qq_fo.sh
adb shell su -c "sh /sdcard/Download/deploy_qq_fo.sh"
adb shell am force-stop com.tencent.mobileqq
echo Redeployed INTERIM fantasywindow.db QQ FO v1 (also keep product bake).
