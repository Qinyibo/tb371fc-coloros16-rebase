@echo off
set PROBE=%~dp0probe
adb push "%PROBE%\fw-native-douyin-v2.db" /sdcard/Download/fw-native-douyin-v2.db
adb push "%PROBE%\deploy_native_v2.sh" /sdcard/Download/deploy_native_v2.sh
adb shell su -c "sh /sdcard/Download/deploy_native_v2.sh"
adb shell am force-stop com.ss.android.ugc.aweme
echo Redeployed native Douyin FO v2.
