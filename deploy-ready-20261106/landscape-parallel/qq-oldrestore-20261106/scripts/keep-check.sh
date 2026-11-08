#!/system/bin/sh
getprop | grep -iE 't2|refresh|sf.' | head -20
md5sum /system_ext/app/OplusFlexibleWindowUI/OplusFlexibleWindowUI.apk 2>/dev/null
ls -l /system_ext/app/OplusFlexibleWindowUI/OplusFlexibleWindowUI.apk
grep -r appSwitchBoostType /my_product/etc 2>/dev/null | head -5