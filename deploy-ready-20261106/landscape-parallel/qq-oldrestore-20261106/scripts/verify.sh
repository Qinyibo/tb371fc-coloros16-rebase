#!/system/bin/sh
am force-stop com.tencent.mobileqq
sleep 1
# landscape free
settings put system user_rotation 1
settings put system accelerometer_rotation 0
monkey -p com.tencent.mobileqq -c android.intent.category.LAUNCHER 1
sleep 5
echo "==== TASK ===="
dumpsys activity activities | grep -E "mobileqq|mode=|TaskFragment|bounds=|mResumedActivity|SplashActivity|EmptyActivity" | head -80
echo "==== WINDOWS ===="
dumpsys window windows | grep -E "mobileqq|mFrame|mHasSurface" | head -40
echo "==== DB ===="
# pull via cp for host later
cp -f /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db /sdcard/Download/fantasywindow.after-oldrestore.db
chmod 644 /sdcard/Download/fantasywindow.after-oldrestore.db
echo DONE_VERIFY