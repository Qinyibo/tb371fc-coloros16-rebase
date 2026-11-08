#!/system/bin/sh
set -e
DB_SRC=/sdcard/Download/fantasywindow.qq-fix.db
DB_DST=/data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db
PID=$(pidof com.oplus.exsystemservice)
echo EXPID=$PID
[ -n "$PID" ] || { echo FAIL no exsystemservice; exit 1; }
[ -f "$DB_SRC" ] || { echo FAIL no db src; exit 2; }
# backup live
su -t $PID -c "cp -f $DB_DST /data/local/tmp/fantasywindow.pre-qqfix.db" || true
cp -f "$DB_DST" /sdcard/Download/fantasywindow.pre-qqfix.db 2>/dev/null || true
su -t $PID -c "cp -f $DB_SRC $DB_DST"
su -t $PID -c "chmod 660 $DB_DST"
su -t $PID -c "chown system:system $DB_DST"
su -t $PID -c "ls -la $DB_DST"
kill -9 $PID
sleep 1
echo NEWPID=$(pidof com.oplus.exsystemservice)
echo OK_DB_QQ_FIX