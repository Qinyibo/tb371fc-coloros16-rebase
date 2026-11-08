@echo off
chcp 65001 >nul
setlocal EnableExtensions
set HERE=%~dp0
set ZIP=%HERE%tb371fc_jingling_office_v21.zip
set APK=%HERE%magisk-module\system\app\YozoOffice\YozoOffice.apk
set MOD=tb371fc_jingling_office_v21
set PKG=com.yozo.office
set EXPECT_SHA=0CC7977DB6C35EAB3DD3E919800B06D59D0035A819F30FA464726AEB5E508461
set REMOTE_ZIP=/data/local/tmp/tb371fc_jingling_office_v21.zip
set SU=/debug_ramdisk/su

echo === jingling-office-v21 one-click flash ===
if not exist "%ZIP%" ( echo FAIL: missing zip - run python build-zip.py & exit /b 1 )
if not exist "%APK%" ( echo FAIL: missing APK & exit /b 1 )

adb get-state 1>nul 2>nul
if errorlevel 1 ( echo FAIL: no adb device & exit /b 1 )
adb shell %SU% -c id 1>nul 2>nul
if errorlevel 1 (
  adb shell su -c id 1>nul 2>nul
  if errorlevel 1 ( echo FAIL: no root & exit /b 1 )
  set SU=su
)

echo [1/5] SHA gate local APK ...
for /f "tokens=1" %%H in ('certutil -hashfile "%APK%" SHA256 ^| findstr /R "^[0-9A-Fa-f][0-9A-Fa-f]*$"') do set LOCAL=%%H
echo local_sha=%LOCAL%
if /I not "%LOCAL%"=="%EXPECT_SHA%" ( echo FAIL: local APK sha mismatch & exit /b 1 )

echo [2/5] push zip ...
adb push "%ZIP%" %REMOTE_ZIP%
if errorlevel 1 exit /b 1

echo [3/5] magisk --install-module ...
adb shell %SU% -c "magisk --install-module %REMOTE_ZIP%"
if errorlevel 1 ( echo FAIL: magisk install & exit /b 1 )

echo [4/5] remove /data user install so Magisk system/app wins after reboot ...
adb shell pm uninstall %PKG% 1>nul 2>nul
adb shell pm uninstall --user 0 %PKG% 1>nul 2>nul

echo [5/5] reboot and verify ...
adb reboot
echo waiting for device boot ...
adb wait-for-device
set /a n=0
:waitboot
set /a n+=1
if %n% GTR 72 goto boottimeout
for /f "tokens=*" %%A in ('adb shell getprop sys.boot_completed 2^>nul') do set BC=%%A
if "%BC%"=="1" goto booted
timeout /t 5 /nobreak >nul
goto waitboot

:booted
echo boot_completed=1
timeout /t 10 /nobreak >nul
call "%HERE%check-verify.cmd"
exit /b %ERRORLEVEL%

:boottimeout
echo WARN: boot_completed timeout; still running verify
call "%HERE%check-verify.cmd"
exit /b %ERRORLEVEL%