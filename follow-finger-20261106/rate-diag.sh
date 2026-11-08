#!/system/bin/sh
grep -Rsn 'R60_90_120' /my_product/etc /odm/etc 2>/dev/null | head -40
grep -Rsn 'defaultRateId' /my_product/etc 2>/dev/null | head -20
grep -Rsn 'extreme' /my_product/etc/permissions 2>/dev/null | head -40
grep -Rsn 'app_extreme_high' /system /system_ext /my_product 2>/dev/null | head -40
getprop | grep -i extreme
pm list features | grep -i extreme
pm list features | grep -i refresh