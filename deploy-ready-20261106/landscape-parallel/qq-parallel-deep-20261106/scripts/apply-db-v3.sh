#!/system/bin/sh
set -e
DB_SRC=/sdcard/Download/fantasywindow.qq-v3.db
DB_DST=/data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db
PID=$(pidof com.oplus.exsystemservice)
echo EXPID=$PID
su -t $PID -c "cp -f $DB_DST /data/local/tmp/fantasywindow.pre-qqv3.db" || true
su -t $PID -c "cp -f $DB_SRC $DB_DST"
su -t $PID -c "chmod 660 $DB_DST"
su -t $PID -c "chown system:system $DB_DST"
kill -9 $PID
sleep 1
echo NEWPID=$(pidof com.oplus.exsystemservice)
echo OK_DB_QQ_V3
