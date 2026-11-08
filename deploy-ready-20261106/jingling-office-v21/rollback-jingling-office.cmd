@echo off
chcp 65001 >nul
setlocal EnableExtensions
set MOD=tb371fc_jingling_office_v21
set PKG=com.yozo.office

echo === jingling-office-v21 rollback ===
adb get-state 1>nul 2>nul
if errorlevel 1 (
  echo FAIL: no adb device
  exit /b 1
)

echo Mark Magisk module for remove and reboot ...
adb shell /debug_ramdisk/su -c "touch /data/adb/modules/%MOD%/remove"
adb shell pm uninstall %PKG% 1>nul 2>nul
adb reboot
adb wait-for-device
timeout /t 25 /nobreak >nul
adb wait-for-device
adb shell "while [ \"$(getprop sys.boot_completed)\" != 1 ]; do sleep 2; done" 2>nul

adb shell /debug_ramdisk/su -c "ls /data/adb/modules/%MOD% 2>/dev/null || echo module_gone=1"
adb shell pm path %PKG% 1>nul 2>nul
if errorlevel 1 (
  echo PASS: package removed
) else (
  echo WARN: package still present - may be leftover /data install
  adb shell pm path %PKG%
)
echo RESULT=ROLLBACK_DONE
echo hardware_success_claimed=false
exit /b 0