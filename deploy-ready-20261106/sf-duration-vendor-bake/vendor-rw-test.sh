#!/system/bin/sh
id
getenforce
grep " /vendor " /proc/mounts | head -1
mount -o remount,rw /vendor
echo remount_rw:$?
grep " /vendor " /proc/mounts | head -1
touch /vendor/.rw_test_agent
echo touch:$?
ls -la /vendor/.rw_test_agent
rm -f /vendor/.rw_test_agent
mount -o remount,ro /vendor
echo remount_ro:$?
grep " /vendor " /proc/mounts | head -1