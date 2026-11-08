#!/system/bin/sh
echo ===MY_PRODUCT_TOUCH_VRR===
ls -la /my_product/etc/ 2>/dev/null | grep -iE 'touch|input|vrr|refresh|frame|screen|adfr|gesture|nvt'
echo ===VENDOR===
ls -la /vendor/etc/ 2>/dev/null | grep -iE 'touch|input|vrr|nvt|gesture' | head -40
find /my_product /odm /vendor/etc -maxdepth 3 -iname '*touch*' 2>/dev/null | head -40
find /my_product /odm /vendor/etc -maxdepth 3 -iname '*nvt*' 2>/dev/null | head -20
find /my_product /odm /vendor/etc -maxdepth 3 -iname '*input*' 2>/dev/null | head -40
echo ===PROPS_TOUCH===
getprop | grep -iE 'touch|nvt|input.dispatcher|sf.phase|refresh|adfr|vrr' | head -80
echo ===IRQ===
cat /proc/interrupts | grep -iE 'nvt|spi|touch|ts' | head -20
