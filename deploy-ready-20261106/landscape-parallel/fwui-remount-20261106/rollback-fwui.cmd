@echo off
set HERE=%~dp0
adb push "%HERE%backup\OplusFlexibleWindowUI-pre.apk" /data/local/tmp/OplusFlexibleWindowUI.restore.apk
adb push "%HERE%backup\OplusFlexibleWindowUI-pre.vdex" /data/local/tmp/OplusFlexibleWindowUI.restore.vdex
adb push "%HERE%rollback-fwui.sh" /data/local/tmp/rollback-fwui.sh
adb shell su -mm -c "sh /data/local/tmp/rollback-fwui.sh"
adb shell am force-stop com.oplus.pscanvas
echo Rolled back FlexibleWindowUI to pre-materials hash 01450E66...
