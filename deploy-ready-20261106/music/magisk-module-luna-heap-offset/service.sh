#!/system/bin/sh
MODDIR=${0%/*}
[ -f "$MODDIR/enable-prefs-watchdog" ] || exit 0
PREF=/data/user/0/com.luna.music/shared_prefs/luna_launch_local_shared_preferences.xml
while true; do
  if [ -f "$PREF" ] && grep -q 'enableArtHeapExpandV4" value="true"' "$PREF"; then
    sed -i 's/enableArtHeapExpandV4" value="true"/enableArtHeapExpandV4" value="false"/' "$PREF"
  fi
  sleep 15
done
