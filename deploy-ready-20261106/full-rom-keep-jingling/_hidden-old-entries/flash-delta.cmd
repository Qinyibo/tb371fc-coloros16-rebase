@echo off
REM ASCII wrapper: recommended delta flash (KEEP baseline, no userdata wipe)
setlocal
set ROOT=%~dp0
set WORK=D:\TB371FC-release\clean-rebase-20261104\pen-sharing-compat\candidate-keep-jingling-20261106
set PY=C:\Program Files\Python312\python.exe
set TOOLS=D:\TB371FC-release\clean-rebase-20261104\tools
echo === KEEP+Jingling delta flash (no userdata wipe) ===
echo Require: physical super still pen-v4-on-e088 KEEP (7b1c6736...)
echo Target: system/app/YozoOffice baked into super
echo.
"%ROOT%tools\adb.exe" devices
echo.
echo Calling flash_candidate_delta.py ...
"%PY%" "%TOOLS%\flash_candidate_delta.py" --work "%WORK%" --receipt "%WORK%\physical-baseline-receipt.json"
set ERR=%ERRORLEVEL%
echo exit=%ERR%
if not %ERR%==0 (
  echo Flash failed. Check attempt-logs / physical-delta-receipt.
  pause
  exit /b %ERR%
)
echo.
echo Flash script returned success. Next: verify.cmd
pause
exit /b 0
