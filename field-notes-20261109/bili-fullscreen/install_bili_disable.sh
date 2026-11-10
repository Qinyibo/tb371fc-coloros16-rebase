#!/system/bin/sh
SRC=/data/local/tmp/sys_fantasy_window_managed.xml
DST=/my_product/etc/fantasy/sys_fantasy_window_managed.xml
BK=/data/adb/tb371fc-capture/backup/sys_fantasy_window_managed.xml.pre_bili_disable
mkdir -p /data/adb/tb371fc-capture/backup
[ -f "$BK" ] || cp "$DST" "$BK"
echo "backup: $(sha256sum "$BK" 2>/dev/null)"
mount -o remount,rw / 2>&1; echo "remount_rc=$?"
cp "$SRC" "$DST" || { echo COPY_FAIL; exit 1; }
chown root:root "$DST"; chmod 644 "$DST"
chcon u:object_r:system_file:s0 "$DST" 2>/dev/null
sync
echo "bili entries left: $(grep -c 'package_name=\"tv.danmaku.bili\"' "$DST")"
sha256sum "$DST" "$SRC"
mount -o remount,ro / 2>&1
