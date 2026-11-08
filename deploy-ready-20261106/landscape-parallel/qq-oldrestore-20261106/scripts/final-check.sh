#!/system/bin/sh
cp -f /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db /sdcard/Download/fantasywindow.live-final.db
chmod 644 /sdcard/Download/fantasywindow.live-final.db
sha256sum /system_ext/app/OplusFlexibleWindowUI/OplusFlexibleWindowUI.apk
grep appSwitchBoostType /my_product/etc/refresh_rate_config.xml
getprop debug.sf.early.app.duration
getprop debug.sf.early.sf.duration
grep -o 'package_name="com.tencent.mobileqq"[^/]*/>' /my_product/etc/fantasy/sys_fantasy_window_managed.xml | head -c 260; echo
grep mobileqq /my_product/etc/fantasy/sys_full_orientation_managed.xml