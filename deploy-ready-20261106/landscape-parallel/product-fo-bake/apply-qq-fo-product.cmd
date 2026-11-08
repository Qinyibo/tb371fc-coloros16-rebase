@echo off
set HERE=%~dp0
adb push "%HERE%sys_full_orientation_managed.qq-fo-v1.xml" /data/local/tmp/sys_full_orientation_managed.qq-fo-v1.xml
adb push "%HERE%apply-qq-fo-product.sh" /data/local/tmp/apply-qq-fo-product.sh
adb shell su -mm -c "sh /data/local/tmp/apply-qq-fo-product.sh"
echo Done product FO bake. DB interim still active until cloud rewrite; product bake survives rebuild seed.
