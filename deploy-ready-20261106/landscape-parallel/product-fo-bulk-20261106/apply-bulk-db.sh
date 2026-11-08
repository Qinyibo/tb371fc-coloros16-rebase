#!/system/bin/sh
set -e
DB_SRC=/sdcard/Download/fantasywindow.bulk-v1.db
DB_DST=/data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db
PID=$(pidof com.oplus.exsystemservice)
echo EXPID=$PID
[ -n "$PID" ] || { echo FAIL no exsystemservice; exit 1; }
[ -f "$DB_SRC" ] || { echo FAIL no db src; exit 2; }
su -t $PID -c "cp -f $DB_SRC $DB_DST"
su -t $PID -c "chmod 660 $DB_DST"
su -t $PID -c "chown system:system $DB_DST"
su -t $PID -c "ls -la $DB_DST"
# backup previous live briefly
cp -f "$DB_SRC" /sdcard/Download/fantasywindow.bulk-v1.applied.db
kill -9 $PID
sleep 1
echo NEWPID=$(pidof com.oplus.exsystemservice)
echo OK_DB_BULK
