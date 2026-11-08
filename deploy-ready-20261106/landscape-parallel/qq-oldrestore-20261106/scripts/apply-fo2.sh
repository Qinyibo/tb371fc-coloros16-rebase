#!/system/bin/sh
set -e
mount -o remount,rw /
cp -f /data/local/tmp/sys_full_orientation_managed.oldrestore.xml /my_product/etc/fantasy/sys_full_orientation_managed.xml
chmod 644 /my_product/etc/fantasy/sys_full_orientation_managed.xml
sync
mount -o remount,ro / 2>/dev/null || true
PID=$(pidof com.oplus.exsystemservice)
su -t $PID -c "cp -f /sdcard/Download/fantasywindow.oldrestore.db /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db"
su -t $PID -c "chmod 660 /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db; chown system:system /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db"
kill -9 $PID
sleep 1
echo FO=$(grep -o 'package_name="com.tencent.mobileqq"[^/]*/>' /my_product/etc/fantasy/sys_full_orientation_managed.xml)
echo NEWPID=$(pidof com.oplus.exsystemservice)
echo OK_FO2