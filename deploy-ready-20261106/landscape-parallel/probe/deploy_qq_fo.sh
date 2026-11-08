#!/system/bin/sh
PID=$(pidof com.oplus.exsystemservice)
echo EXPID=$PID
su -t $PID -c 'cp -f /sdcard/Download/fw-native-qq-v1.db /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'
su -t $PID -c 'chmod 660 /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'
su -t $PID -c 'chown system:system /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'
su -t $PID -c 'ls -la /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'
kill -9 $PID
sleep 1
echo NEWPID=$(pidof com.oplus.exsystemservice)
