@echo off
chcp 936 >nul
echo.
echo 请双击 ASCII 入口，避免中文文件名编码问题：
echo   推荐一键：FLASH.cmd   （完整 ROM：super/boot/vbmeta，不清 userdata）
echo   连接检查：check1.cmd
echo   刷前检查：check2.cmd
echo   完整super：flash-full.cmd
echo   delta刷入：flash-delta.cmd  （仅变动块，非整包）
echo   刷后核验：verify.cmd
echo.
pause
