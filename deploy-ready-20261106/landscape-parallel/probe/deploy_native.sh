PID=$(pidof com.oplus.exsystemservice)
echo EXPID=$PID
cp -f /sdcard/Download/fw-native-douyin.db /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db
chown system:system /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db
chmod 660 /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db
restorecon /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db 2>/dev/null
kill -9 $PID
sleep 1
echo NEWPID=$(pidof com.oplus.exsystemservice)
