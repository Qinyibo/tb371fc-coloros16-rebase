@echo off
REM ASCII wrapper: pre-flash device check (no flash)
setlocal
set ROOT=%~dp0
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%ROOT%scripts\Invoke-R91-Clean.ps1" -CheckDevice
set result=%errorlevel%
echo.
echo Pre-flash check finished. Do not flash if errors appeared above.
pause
exit /b %result%
