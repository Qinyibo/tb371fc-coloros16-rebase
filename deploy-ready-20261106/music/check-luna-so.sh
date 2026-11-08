#!/system/bin/sh
for f in /data/app/*/com.luna.music*/lib/arm64/libsysoptimizer.so /data/app/*/*/lib/arm64/libsysoptimizer.so; do
  [ -f "$f" ] || continue
  echo "$f" | grep -q com.luna.music || continue
  echo "FILE=$f"
  sha256sum "$f"
  ls -la "$f"
done
echo "MODULE_SO:"
sha256sum /data/adb/modules/tb371fc_luna_heap_offset_fix/lib/libsysoptimizer.so
ls -la /data/adb/modules/tb371fc_luna_heap_offset_fix/
ls -la /data/adb/modules/tb371fc_luna_heap_offset_fix/lib/