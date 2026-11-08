#!/system/bin/sh
echo ===DMESG_NVT===
dmesg 2>/dev/null | grep -iE 'nvt|novatek|report.?rate|touch.*Hz|Hz.*touch|SPI.*touch' | tail -80
echo ===LOGCAT_NVT===
logcat -d -b all -t 200 | grep -iE 'NVT|novatek|TouchReport|report_rate|InputReader|InputDispatcher' | tail -40
echo ===DT_REPORT===
find /proc/device-tree -iname '*nvt*' 2>/dev/null | head
find /sys/firmware/devicetree -iname '*nvt*' 2>/dev/null | head
for n in $(find /sys/firmware/devicetree -iname '*report*' 2>/dev/null | head -30); do echo FILE $n; xxd "$n" 2>/dev/null | head -2; done
echo ===STRINGS_VENDOR_TOUCH===
find /vendor /odm /my_product -iname '*touch*' 2>/dev/null | head -40
ls -la /vendor/firmware/*nvt* /odm/firmware/*nvt* /vendor/firmware/*NVT* 2>/dev/null | head
echo ===GETEVENT_PERMS===
ls -la /dev/input/event4
id
