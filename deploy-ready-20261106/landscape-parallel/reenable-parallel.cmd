@echo off
REM Re-enable parallel windows + COSA (run from host with adb)
adb shell pm enable --user 0 com.oplus.pscanvas
adb shell pm enable --user 0 com.oplus.cosa
echo Done. Open ?? and search ????, or:
echo   adb shell su -c "am start -n com.oplus.pscanvas/com.oplus.flexibletask.setting.SettingActivity"
