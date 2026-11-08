@echo off
REM Undo landscape-parallel restore (disable again)
adb shell pm disable-user --user 0 com.oplus.pscanvas
adb shell pm disable-user --user 0 com.oplus.cosa
