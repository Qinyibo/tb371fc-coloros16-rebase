#!/system/bin/sh
grep -iE "pad|tablet|dpi|density|land|split|dual|fold|mode" /data/user/0/com.tencent.mobileqq/shared_prefs/com.tencent.mobileqq_preferences.xml | head -60
echo ----
wm density
wm size
getprop ro.sf.lcd_density
getprop persist.sys.density