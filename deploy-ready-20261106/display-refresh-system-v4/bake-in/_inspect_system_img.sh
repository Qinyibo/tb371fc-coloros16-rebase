#!/bin/bash
set -e
SYS=/mnt/d/TB371FC-release/clean-rebase-20261104/integrated-logicals/system.img
M=/tmp/sys-inspect-refresh
mkdir -p "$M"
sudo mount -o ro,loop "$SYS" "$M"
echo MOUNTED
ls -la "$M/my_product/etc/refresh_rate_config.xml"
md5sum "$M/my_product/etc/refresh_rate_config.xml"
df -h "$M"
ls -ld "$M/my_product" "$M/my_heytap" "$M/my_stock" 2>&1 | head
# also check base-ext4
sudo umount "$M"
BASE=/mnt/d/TB371FC-release/clean-rebase-20261104/base-ext4-UNADAPTED/system.img
sudo mount -o ro,loop "$BASE" "$M"
echo BASE_MOUNTED
ls -la "$M/my_product/etc/refresh_rate_config.xml" 2>&1
md5sum "$M/my_product/etc/refresh_rate_config.xml" 2>&1
sudo umount "$M"
rmdir "$M"
echo DONE
