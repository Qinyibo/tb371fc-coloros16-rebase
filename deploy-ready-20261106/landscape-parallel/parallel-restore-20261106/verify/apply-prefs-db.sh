#!/system/bin/sh
set -e
PID=$(pidof com.oplus.exsystemservice)
echo EXPID=$PID
[ -n "$PID" ] || exit 1
su -t $PID -c "cp -f /data/local/tmp/fantasy_window_prefs.aligned.xml /data/user_de/0/com.oplus.exsystemservice/shared_prefs/fantasy_window_prefs.xml"
su -t $PID -c "chmod 660 /data/user_de/0/com.oplus.exsystemservice/shared_prefs/fantasy_window_prefs.xml"
su -t $PID -c "cat /data/user_de/0/com.oplus.exsystemservice/shared_prefs/fantasy_window_prefs.xml"
# also ensure DB still parallel-v2
su -t $PID -c "cp -f /sdcard/Download/fantasywindow.parallel-v1.db /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db"
su -t $PID -c "chmod 660 /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db"
kill -9 $PID
sleep 1
echo NEWPID=$(pidof com.oplus.exsystemservice)
echo OK_PREFS_DB