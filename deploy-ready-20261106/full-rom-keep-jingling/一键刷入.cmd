@echo off
chcp 936 >nul
setlocal
cd /d "%~dp0"
echo === 一键刷入：完整 ROM（super/boot/vbmeta）===
echo 不清 userdata（保留 Magisk/账号/数据）
echo 请确认：已解锁、电量充足、仅连接本机 TB371FC
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\Invoke-R91-Clean.ps1" -Execute -Reboot
set ERR=%ERRORLEVEL%
echo.
echo exit=%ERR%
if not %ERR%==0 (
  echo 刷入失败，请查看 attempt-logs 最新目录。
) else (
  echo 刷入命令已完成。开机后可用 核验ROM.cmd 检查鲸鲮。
)
pause
exit /b %ERR%