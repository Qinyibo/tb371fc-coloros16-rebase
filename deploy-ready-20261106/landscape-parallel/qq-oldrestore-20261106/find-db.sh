#!/system/bin/sh
find /data -name 'fantasywindow.db' 2>/dev/null
find /data -name '*fantasy*' 2>/dev/null | head -40
ls -la /data/data/com.oplus.exsystemservice/databases/ 2>/dev/null
ls -la /data/user_de/0/com.oplus.exsystemservice/databases/ 2>/dev/null