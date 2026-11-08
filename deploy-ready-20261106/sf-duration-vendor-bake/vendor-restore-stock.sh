#!/system/bin/sh
set -e
STOCK=/data/local/tmp/build.prop.stock
ALT=/data/adb/sf_duration_rollback/build.prop.stock
TARGET=/vendor/build.prop
if [ ! -f "$STOCK" ]; then STOCK="$ALT"; fi
test -f "$STOCK" || { echo missing stock; exit 1; }
mount -o remount,rw /vendor
cp -f "$STOCK" "$TARGET"
chmod 600 "$TARGET"
chown root:root "$TARGET"
chcon u:object_r:vendor_file:s0 "$TARGET" 2>/dev/null || true
sync
md5sum "$TARGET"
grep -E 'high_fps|duration|use_phase' "$TARGET" || true
mount -o remount,ro /vendor
rm -f /data/local/tmp/vendor_prop_trial.flag
echo RESTORED_OK
