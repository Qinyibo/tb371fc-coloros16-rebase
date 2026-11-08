#!/system/bin/sh
MOD=/data/adb/modules/tb371fc_luna_heap_offset_fix
set -e
mkdir -p "$MOD/lib"
# broken Windows-style literal backslash filename
SRC="$MOD/lib\libsysoptimizer.so"
DST="$MOD/lib/libsysoptimizer.so"
if [ ! -f "$SRC" ]; then
  echo "MISSING_SRC"
  ls -la "$MOD"
  exit 1
fi
cp -f "$SRC" "$DST"
chmod 644 "$DST"
echo "DST_SHA=$(sha256sum "$DST" | cut -d' ' -f1)"
# clean broken junk after successful copy
rm -f "$MOD/lib\libsysoptimizer.so"
rm -f "$MOD/META-INF\com\google\android\update-binary"
rm -f "$MOD/META-INF\com\google\android\updater-script"
rm -f "$MOD/system\\"
rmdir "$MOD/system" 2>/dev/null || true
echo "AFTER_LAYOUT:"
ls -la "$MOD"
ls -la "$MOD/lib"
find "$MOD" -print