@echo off
chcp 936 >nul
echo === ºËÑé ROM / ¾¨öì ===
"%~dp0tools\adb.exe" wait-for-device
"%~dp0tools\adb.exe" shell getprop sys.boot_completed
"%~dp0tools\adb.exe" shell pm path com.yozo.office
"%~dp0tools\adb.exe" shell ls -l /system/app/YozoOffice/YozoOffice.apk
pause