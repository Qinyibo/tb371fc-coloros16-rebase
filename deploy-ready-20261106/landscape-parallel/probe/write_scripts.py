from pathlib import Path
base=Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel")
probe=base/"probe"
# rollback restores fantasywindow.db.bak (pre magic patch) OR before-native
script=r'''@echo off
REM Rollback Douyin fantasy DB to pre-native (magic=2 exclude PAD, fullorient=2 stock)
REM Asia/Hong_Kong
set PROBE=%~dp0probe
adb push "%PROBE%\fantasywindow.db.bak" /sdcard/Download/fantasywindow.db.bak
adb shell "su -c \"PID=$(pidof com.oplus.exsystemservice); su -t $PID -c 'cp -f /sdcard/Download/fantasywindow.db.bak /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'; su -t $PID -c 'chmod 660 /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'; kill -9 $PID\""
echo Rolled back fantasywindow.db to stock bak. Force-stop Douyin yourself.
'''
# simpler bat without nested hell - use sh
sh='''#!/system/bin/sh
PID=$(pidof com.oplus.exsystemservice)
echo EXPID=$PID
su -t $PID -c 'cp -f /sdcard/Download/fantasywindow.db.bak /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'
su -t $PID -c 'chmod 660 /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'
kill -9 $PID
sleep 1
echo NEWPID=$(pidof com.oplus.exsystemservice)
'''
(probe/"rollback-native.sh").write_text(sh, encoding='utf-8', newline='\n')
bat='''@echo off
setlocal
set PROBE=%~dp0probe
adb push "%PROBE%\\fantasywindow.db.bak" /sdcard/Download/fantasywindow.db.bak
adb push "%PROBE%\\rollback-native.sh" /sdcard/Download/rollback-native.sh
adb shell su -c "sh /sdcard/Download/rollback-native.sh"
echo Done. am force-stop com.ss.android.ugc.aweme then relaunch.
'''
(base/"rollback-douyin-native.cmd").write_text(bat, encoding='utf-8', newline='\r\n')
# redeploy native v2 helper
dep='''#!/system/bin/sh
PID=$(pidof com.oplus.exsystemservice)
echo EXPID=$PID
su -t $PID -c 'cp -f /sdcard/Download/fw-native-douyin-v2.db /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'
su -t $PID -c 'chmod 660 /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'
su -t $PID -c 'ls -la /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db'
kill -9 $PID
sleep 1
echo NEWPID=$(pidof com.oplus.exsystemservice)
'''
(probe/"deploy_native_v2.sh").write_text(dep, encoding='utf-8', newline='\n')
bat2='''@echo off
set PROBE=%~dp0probe
adb push "%PROBE%\\fw-native-douyin-v2.db" /sdcard/Download/fw-native-douyin-v2.db
adb push "%PROBE%\\deploy_native_v2.sh" /sdcard/Download/deploy_native_v2.sh
adb shell su -c "sh /sdcard/Download/deploy_native_v2.sh"
adb shell am force-stop com.ss.android.ugc.aweme
echo Redeployed native Douyin FO v2.
'''
(base/"redeploy-douyin-native.cmd").write_text(bat2, encoding='utf-8', newline='\r\n')
print('scripts ok')
