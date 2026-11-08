#!/system/bin/sh
sha256sum /system_ext/app/OplusFlexibleWindowUI/OplusFlexibleWindowUI.apk
uiautomator dump /sdcard/Download/qq-ui.xml >/dev/null 2>&1
wc -c /sdcard/Download/qq-ui.xml
# sample dual markers
grep -oE 'text="[^"]{0,40}"' /sdcard/Download/qq-ui.xml | head -40
grep -c 'bounds=' /sdcard/Download/qq-ui.xml