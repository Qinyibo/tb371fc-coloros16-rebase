@echo off
REM ASCII wrapper: full super flash (wipe_userdata=false)
setlocal
set ROOT=%~dp0
echo === Full super flash (keep userdata: wipe=false) ===
echo Will write super/boot/vbmeta. Confirm unlocked device and enough battery.
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%ROOT%scripts\Invoke-R91-Clean.ps1" -Execute -Reboot
set ERR=%ERRORLEVEL%
echo exit=%ERR%
pause
exit /b %ERR%
