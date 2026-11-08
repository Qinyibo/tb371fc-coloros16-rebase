#!/system/bin/sh
# live-bake-refresh-xml.sh — write proven refresh XML into system /my_product tree
# Asia/Hong_Kong. Does not flash partitions. Requires root (su).
set -e
SRC=/data/local/tmp/refresh_rate_config.xml
TARGET=/my_product/etc/refresh_rate_config.xml
EXPECT=35db38f8c85758c372546c707513642c
STOCK_EXPECT=7e48f867e573a1e207471805e3d03902
MOD=/data/adb/modules/tb371fc_system_refresh_policy
STAMP=$(date +%Y%m%d-%H%M%S)
BAK=/data/local/tmp/refresh_rate_config.xml.stock-$STAMP

id | grep -q 'uid=0' || { echo "FAIL need root (uid=0)"; exit 1; }

if [ ! -f "$SRC" ]; then
  echo "FAIL missing $SRC"
  exit 1
fi
ACT=$(md5sum "$SRC" | awk '{print $1}')
if [ "$ACT" != "$EXPECT" ]; then
  echo "FAIL src md5 $ACT != $EXPECT"
  exit 1
fi

echo "PRE mount_bind_line=$(mount | grep refresh_rate || echo NONE)"
echo "PRE target_md5_with_possible_bind=$(md5sum "$TARGET" 2>/dev/null | awk '{print $1}' || echo MISSING)"
echo "PRE magisk_disable_exists=$([ -f "$MOD/disable" ] && echo YES || echo NO)"
echo "PRE magisk_module_dir=$([ -d "$MOD" ] && echo YES || echo NO)"

# Drop Magisk file-bind so we see/write the real system-tree file
umount "$TARGET" 2>/dev/null || true
sleep 0.2
echo "POST_UMOUNT mount_bind_line=$(mount | grep refresh_rate || echo NONE)"
UNDER=$(md5sum "$TARGET" 2>/dev/null | awk '{print $1}' || echo MISSING)
echo "POST_UMOUNT underlying_md5=$UNDER"

# Backup underlying (expect stock unless already baked)
cp -f "$TARGET" "$BAK"
chmod 644 "$BAK"
echo "BACKUP path=$BAK md5=$(md5sum "$BAK" | awk '{print $1}') size=$(wc -c < "$BAK")"

# Remount system root rw (dm-2 / holds /my_product)
if ! mount -o remount,rw /; then
  echo "FAIL remount rw /"
  exit 2
fi
echo "REMOUNT_RW ok"

if ! cp -f "$SRC" "$TARGET"; then
  echo "FAIL cp to $TARGET — attempting remount ro"
  mount -o remount,ro / 2>/dev/null || true
  exit 3
fi
chmod 644 "$TARGET"
chown root:root "$TARGET"
restorecon -v "$TARGET" || true
sync

FINAL=$(md5sum "$TARGET" | awk '{print $1}')
echo "WRITTEN md5=$FINAL"
if [ "$FINAL" != "$EXPECT" ]; then
  echo "FAIL written md5 $FINAL != $EXPECT — restoring backup"
  cp -f "$BAK" "$TARGET" || true
  chmod 644 "$TARGET" || true
  sync
  mount -o remount,ro / 2>/dev/null || true
  exit 4
fi

mount -o remount,ro / 2>/dev/null || echo "WARN remount ro failed (non-fatal)"

# Disable Magisk refresh so ABA sees ROM/system content
if [ -d "$MOD" ]; then
  touch "$MOD/disable"
  echo "MAGISK_DISABLE touched"
else
  echo "MAGISK_MODULE_ABSENT (ok)"
fi

echo "BAKED md5=$FINAL"
echo "mount_bind_line=$(mount | grep refresh_rate || echo NONE)"
echo "BACKUP_HOST_PULL=$BAK"
echo "NEXT: reboot then ABA; hardware_success_claimed stays false until subjective fluency"