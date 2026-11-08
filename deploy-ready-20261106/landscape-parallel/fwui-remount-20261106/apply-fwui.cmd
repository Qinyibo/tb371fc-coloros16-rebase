@echo off
set HERE=%~dp0
adb push "%HERE%payload\OplusFlexibleWindowUI.apk" /data/local/tmp/OplusFlexibleWindowUI.new.apk
adb push "%HERE%payload\OplusFlexibleWindowUI.vdex" /data/local/tmp/OplusFlexibleWindowUI.new.vdex
adb push "%HERE%apply-fwui-remount.sh" /data/local/tmp/apply-fwui-remount.sh
adb shell su -mm -c "sh /data/local/tmp/apply-fwui-remount.sh"
adb shell am force-stop com.oplus.pscanvas
echo Applied old R94 FlexibleWindowUI SHA 19D32858...
