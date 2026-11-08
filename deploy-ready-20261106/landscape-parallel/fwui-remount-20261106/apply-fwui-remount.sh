set -e
echo "ns=$(readlink /proc/self/ns/mnt)"
mount -o rw,remount /system_ext
mount | grep ' /system_ext '
mkdir -p /data/local/tmp/fwui-bak-20261106
cp -a /system_ext/app/OplusFlexibleWindowUI/OplusFlexibleWindowUI.apk /data/local/tmp/fwui-bak-20261106/
cp -a /system_ext/app/OplusFlexibleWindowUI/oat/arm64/OplusFlexibleWindowUI.vdex /data/local/tmp/fwui-bak-20261106/ || true
cp /data/local/tmp/OplusFlexibleWindowUI.new.apk /system_ext/app/OplusFlexibleWindowUI/OplusFlexibleWindowUI.apk
cp /data/local/tmp/OplusFlexibleWindowUI.new.vdex /system_ext/app/OplusFlexibleWindowUI/oat/arm64/OplusFlexibleWindowUI.vdex
chmod 644 /system_ext/app/OplusFlexibleWindowUI/OplusFlexibleWindowUI.apk
chmod 644 /system_ext/app/OplusFlexibleWindowUI/oat/arm64/OplusFlexibleWindowUI.vdex
rm -f /system_ext/app/OplusFlexibleWindowUI/oat/arm64/OplusFlexibleWindowUI.odex /system_ext/app/OplusFlexibleWindowUI/oat/arm64/OplusFlexibleWindowUI.art || true
sync
sha256sum /system_ext/app/OplusFlexibleWindowUI/OplusFlexibleWindowUI.apk
ls -la /system_ext/app/OplusFlexibleWindowUI/ /system_ext/app/OplusFlexibleWindowUI/oat/arm64/
mount -o ro,remount /system_ext
echo DONE