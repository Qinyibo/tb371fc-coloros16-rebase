#!/system/bin/sh
# One init-owned API19 companion; no Magisk module installation or restart loop.
set -eu
DIR=/system_ext/etc/tb371fc-speaker
LIB=/system_ext/lib64/libtb371fc_speaker.so
STATE=/data/adb/r94-speaker-direction-v19
test ! -L "$STATE" || exit 20
umask 077
mkdir -p "$STATE"
chmod 700 "$STATE"
exec >>"$STATE/runtime.log" 2>&1
echo "TB371FC_SPEAKER_START boot=$(cat /proc/sys/kernel/random/boot_id)"
test "$(getprop ro.product.board)" = spinel || exit 20
test "$(cat /sys/module/tfa98xx_dlkm/parameters/fw_name)" = tfa98xx_QS.cnt || exit 20
test "$(sha256sum /vendor/firmware/tfa98xx_QS.cnt | cut -d ' ' -f 1)" = a3f641609cbb617ea2c3169e5a9edc6c04f89a342e99fd96dacc44f216cdfa81 || exit 20
test "$(sha256sum "$DIR/direction.jar" | cut -d ' ' -f 1)" = d11f3cf3e9fb8739c1a25c2e48a5cd266a4f07a1d97fdf3b820d606bfe835add || exit 20
test "$(sha256sum "$LIB" | cut -d ' ' -f 1)" = c32f9b49c8a1e4aadd06ea72bcefdc8283f321c71a06a14d7e0b4a705f4aa675 || exit 20
test "$(sha256sum "$DIR/directionctl" | cut -d ' ' -f 1)" = a4cdf0686a98d8dc455b3543b8bb71c27d3bef0b74d538c9741645ff67b7d679 || exit 20
rm -f "$STATE/stop"
CLASSPATH="$DIR/direction.jar" /system/bin/logwrapper /system/bin/app_process -Djava.library.path=/system_ext/lib64 /system/bin R94SpeakerDirection "$LIB" &
child=$!
trap 'kill -TERM "$child" 2>/dev/null || true' TERM INT
set +e
wait "$child"
result=$?
# Native exclusive ownership ends with the child. Recover only our ledger;
# the driver refuses stale/foreign profile ownership and reports real errors.
"$DIR/directionctl" --restore
restored=$?
echo "TB371FC_SPEAKER_EXIT child=$result restored=$restored"
test "$restored" = 0 || exit 21
exit "$result"
