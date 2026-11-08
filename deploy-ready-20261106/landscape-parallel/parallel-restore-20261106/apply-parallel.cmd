@echo off
set ROOT=%~dp0
adb push "%ROOT%sys_full_orientation_managed.parallel-v1.xml" /data/local/tmp/sys_full_orientation_managed.parallel-v1.xml
adb push "%ROOT%sys_fantasy_window_managed.parallel-v1.xml" /data/local/tmp/sys_fantasy_window_managed.parallel-v1.xml
adb push "%ROOT%apply-product.sh" /data/local/tmp/apply-parallel-product.sh
adb shell "su -c 'chmod 755 /data/local/tmp/apply-parallel-product.sh && /data/local/tmp/apply-parallel-product.sh'"
adb push "%ROOT%fantasywindow.parallel-v1.db" /sdcard/Download/fantasywindow.parallel-v1.db
adb push "%ROOT%apply-db.sh" /data/local/tmp/apply-parallel-db.sh
adb shell "su -c 'chmod 755 /data/local/tmp/apply-parallel-db.sh && /data/local/tmp/apply-parallel-db.sh'"
echo DONE_APPLY_PARALLEL
