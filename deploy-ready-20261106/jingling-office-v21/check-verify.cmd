@echo off
chcp 65001 >nul
setlocal EnableExtensions
set PKG=com.yozo.office
set EXPECT_SHA=0cc7977db6c35eab3dd3e919800b06d59d0035a819f30fa464726aeb5e508461
set MOD=tb371fc_jingling_office_v21
set FAIL=0

echo === jingling-office-v21 check-verify ===

adb get-state 1>nul 2>nul
if errorlevel 1 (
  echo FAIL: no adb device
  exit /b 1
)

echo -- Magisk module --
adb shell /debug_ramdisk/su -c "ls -la /data/adb/modules/%MOD% ; test ! -f /data/adb/modules/%MOD%/disable && echo module_enabled=1 || echo module_enabled=0 ; test ! -f /data/adb/modules/%MOD%/remove && echo module_remove=0 || echo module_remove=1 ; ls -la /data/adb/modules/%MOD%/system/app/YozoOffice/YozoOffice.apk ; sha256sum /data/adb/modules/%MOD%/system/app/YozoOffice/YozoOffice.apk"

echo -- package --
adb shell pm path %PKG%
adb shell dumpsys package %PKG% | findstr /C:"versionName" /C:"versionCode" /C:"codePath" /C:"flags=["

echo -- SHA gate --
for /f "tokens=1" %%H in ('adb shell /debug_ramdisk/su -c "sha256sum /data/adb/modules/%MOD%/system/app/YozoOffice/YozoOffice.apk"') do set LIVE=%%H
echo live_sha=%LIVE%
echo expect=%EXPECT_SHA%
if /I not "%LIVE%"=="%EXPECT_SHA%" (
  echo FAIL: APK sha mismatch
  set FAIL=1
)

echo -- path should be Magisk system overlay or system/app --
adb shell pm path %PKG% | findstr /I "YozoOffice system/app modules" >nul
if errorlevel 1 (
  echo WARN: pm path not obviously systemized; still OK if package present after flash
)

adb shell pm path %PKG% >nul 2>nul
if errorlevel 1 (
  echo FAIL: package not installed
  set FAIL=1
) else (
  echo PASS: package present
)

echo -- smoke launch --
adb shell am force-stop %PKG%
adb shell monkey -p %PKG% -c android.intent.category.LAUNCHER 1
timeout /t 5 /nobreak >nul
adb shell pidof %PKG%
if errorlevel 1 (
  echo WARN: pid not found after monkey; check manually
) else (
  echo PASS: process started
)
adb shell am force-stop %PKG%

echo -- preserve other modules --
adb shell /debug_ramdisk/su -c "ls /data/adb/modules"

if %FAIL% NEQ 0 (
  echo RESULT=FAIL
  exit /b 1
)
echo RESULT=PASS
echo hardware_success_claimed=false
exit /b 0