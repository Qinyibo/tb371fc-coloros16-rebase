#!/system/bin/sh
set -e
STOCK=/data/local/tmp/build.prop.stock
PATCH=/data/local/tmp/build.prop.trial-patched
TARGET=/vendor/build.prop
FLAG=/data/local/tmp/vendor_prop_trial.flag
LABEL=${1:-trial}

echo "LABEL=$LABEL"
echo "pre md5:"; md5sum "$TARGET" "$STOCK" "$PATCH"
test -f "$STOCK" || { echo missing stock; exit 1; }
test -f "$PATCH" || { echo missing patch; exit 1; }
mkdir -p /data/adb/sf_duration_rollback
cp -a "$STOCK" /data/adb/sf_duration_rollback/build.prop.stock
chmod 644 /data/adb/sf_duration_rollback/build.prop.stock
mount -o remount,rw /vendor
echo remount_rw:$?
cp -f "$PATCH" "$TARGET"
chmod 600 "$TARGET"
chown root:root "$TARGET"
chcon u:object_r:vendor_file:s0 "$TARGET" 2>/dev/null || true
sync
echo "post md5:"; md5sum "$TARGET"
echo "sf keys:"; grep -E 'high_fps|duration|use_phase|enable_advanced_sf' "$TARGET"
ls -lZ "$TARGET"
mount -o remount,ro /vendor
echo remount_ro:$?
grep " /vendor " /proc/mounts | head -1
echo "$LABEL $(date +%s)" > "$FLAG"
echo APPLIED_OK