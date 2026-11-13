#!/system/bin/sh
SRC=/data/local/tmp/vendor.qti.hardware.tinno_keyboard@1.0-service.xml
DST=/vendor/etc/vintf/manifest/vendor.qti.hardware.tinno_keyboard@1.0-service.xml
mount -o remount,rw /vendor 2>&1; echo "remount_rc=$?"
cp "$SRC" "$DST" || { echo COPY_FAIL; exit 1; }
chown root:root "$DST"; chmod 644 "$DST"
chcon u:object_r:vendor_configs_file:s0 "$DST" 2>/dev/null
sync
ls -lZ "$DST"
mount -o remount,ro /vendor 2>&1
