set -e
mount -o rw,remount /system_ext
cp /data/local/tmp/OplusFlexibleWindowUI.restore.apk /system_ext/app/OplusFlexibleWindowUI/OplusFlexibleWindowUI.apk
cp /data/local/tmp/OplusFlexibleWindowUI.restore.vdex /system_ext/app/OplusFlexibleWindowUI/oat/arm64/OplusFlexibleWindowUI.vdex
chmod 644 /system_ext/app/OplusFlexibleWindowUI/OplusFlexibleWindowUI.apk
chmod 644 /system_ext/app/OplusFlexibleWindowUI/oat/arm64/OplusFlexibleWindowUI.vdex
sync
sha256sum /system_ext/app/OplusFlexibleWindowUI/OplusFlexibleWindowUI.apk
mount -o ro,remount /system_ext
echo ROLLBACK_DONE