@echo off
REM ASCII wrapper: post-flash verify KEEP + Jingling
setlocal
set ROOT=%~dp0
set ADB=%ROOT%tools\adb.exe
echo === Verify KEEP + Jingling ===
"%ADB%" wait-for-device
"%ADB%" shell getprop sys.boot_completed
"%ADB%" shell getprop ro.build.display.id
"%ADB%" shell pm path com.yozo.office
"%ADB%" shell "ls -la /system/app/YozoOffice/YozoOffice.apk"
"%ADB%" shell "su -c 'md5sum /system/app/YozoOffice/YozoOffice.apk; md5sum /my_product/etc/refresh_rate_config.xml; getenforce; magisk --path'"
"%ADB%" shell dumpsys package com.yozo.office | findstr /i "versionName versionCode codePath system"
echo.
echo Expect: codePath -^> /system/app/YozoOffice ; refresh XML 35db38f8... when no Magisk overlay
echo hardware_success_claimed=false
pause
exit /b 0
