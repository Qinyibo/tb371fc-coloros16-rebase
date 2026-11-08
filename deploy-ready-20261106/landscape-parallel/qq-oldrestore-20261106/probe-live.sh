#!/system/bin/sh
export PATH=/system/bin:/system/xbin:/data/local/tmp:$PATH
DB=/data/system/oplus_flexiblewindow/fantasywindow.db
SQL=/system/bin/sqlite3
[ -x $SQL ] || SQL=/system/xbin/sqlite3
[ -x $SQL ] || SQL=$(ls /apex/*/bin/sqlite3 2>/dev/null | head -1)
echo "SQL=$SQL"
echo "==== MAGIC ===="
$SQL $DB "SELECT package_name,status,custom_mode,length(config),length(custom_config_body) FROM t_config WHERE package_name='com.tencent.mobileqq' AND use_function='magicwindow';"
echo "==== MAGIC CFG ===="
$SQL $DB "SELECT config FROM t_config WHERE package_name='com.tencent.mobileqq' AND use_function='magicwindow';"
echo "==== MAGIC BODY ===="
$SQL $DB "SELECT custom_config_body FROM t_config WHERE package_name='com.tencent.mobileqq' AND use_function='magicwindow';"
echo "==== FO ===="
$SQL $DB "SELECT status,custom_mode,custom_config_body FROM t_config WHERE package_name='com.tencent.mobileqq' AND use_function='fullorientation';"
echo "==== PREFS ===="
grep -E "mobileqq|parallel|magic" /data/user_de/0/com.android.systemui/shared_prefs/* 2>/dev/null | head
dumpsys activity provider com.oplus.exsystemservice 2>/dev/null | head -5
ls -l /data/system/oplus_flexiblewindow/