@echo off
REM ASCII wrapper: connection check (no flash)
setlocal
set ROOT=%~dp0
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%ROOT%scripts\Check-Connection.ps1"
set result=%errorlevel%
echo.
echo Connection check finished. Device should appear in adb or fastboot list.
pause
exit /b %result%
