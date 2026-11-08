from pathlib import Path
p = Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\deploy_native2.sh")
p.write_text("""#!/system/bin/sh
PID=$(pidof com.oplus.exsystemservice)
echo EXPID=$PID
# write as exsystemservice context
su -t $PID -c 'cp -f /sdcard/Download/fw-native-douyin.db /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'
su -t $PID -c 'chmod 660 /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'
# verify size
su -t $PID -c 'ls -la /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'
kill -9 $PID
sleep 1
echo NEWPID=$(pidof com.oplus.exsystemservice)
""", encoding="utf-8", newline="\n")
print("wrote", p)
