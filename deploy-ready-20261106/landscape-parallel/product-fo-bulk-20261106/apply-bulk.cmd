@echo off
set HERE=%~dp0
adb push "%HERE%sys_full_orientation_managed.bulk-v1.xml" /data/local/tmp/sys_full_orientation_managed.bulk-v1.xml
adb push "%HERE%sys_fantasy_window_managed.bulk-v1.xml" /data/local/tmp/sys_fantasy_window_managed.bulk-v1.xml
adb push "%HERE%sys_full_orientation_managed.pre-bulk.xml" /data/local/tmp/sys_full_orientation_managed.pre-bulk.xml
adb push "%HERE%sys_fantasy_window_managed.pre-bulk.xml" /data/local/tmp/sys_fantasy_window_managed.pre-bulk.xml
adb push "%HERE%apply-bulk-product.sh" /data/local/tmp/apply-bulk-product.sh
adb shell su -mm -c "sh /data/local/tmp/apply-bulk-product.sh"
adb push "%HERE%fantasywindow.bulk-v1.db" /sdcard/Download/fantasywindow.bulk-v1.db
adb push "%HERE%apply-bulk-db.sh" /sdcard/Download/apply-bulk-db.sh
adb shell su -c "sh /sdcard/Download/apply-bulk-db.sh"
adb shell am force-stop com.tencent.mm
adb shell am force-stop com.tencent.mobileqq
adb shell am force-stop com.ss.android.ugc.aweme
adb shell am force-stop com.heytap.browser
adb shell am force-stop com.heytap.yoli
echo Done bulk FO product + DB. Verify landscape on sample apps.
