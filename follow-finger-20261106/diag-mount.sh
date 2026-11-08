#!/system/bin/sh
echo "=== xml mount ==="
wc -c /my_product/etc/refresh_rate_config.xml
grep -n "<config " /my_product/etc/refresh_rate_config.xml | head -3
echo "=== xxd head ==="
xxd /data/adb/modules/tb371fc_system_refresh_policy/refresh_rate_config.xml | head -4
echo "=== post-fs ==="
cat /data/adb/modules/tb371fc_system_refresh_policy/post-fs-data.sh
echo "=== mount ==="
mount | grep refresh
ls -l /my_product/etc/refresh_rate_config.xml
