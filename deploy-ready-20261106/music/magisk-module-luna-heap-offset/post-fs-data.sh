#!/system/bin/sh
MODDIR=${0%/*}
TARGET_SHA=e8357c10cef28edb36ad59faeec51d120c9ae41f04ff3de8f5874349dc5f7ec3
PATCHED_SHA=be0565463b741685bdf95803fbb9d5de57832ad862b5e66555df2df7ecc66416
PATCHED="$MODDIR/lib/libsysoptimizer.so"
[ -f "$PATCHED" ] || exit 0
for f in /data/app/*/com.luna.music*/lib/arm64/libsysoptimizer.so /data/app/*/*/lib/arm64/libsysoptimizer.so; do
  [ -f "$f" ] || continue
  cur=$(sha256sum "$f" | cut -d' ' -f1)
  if [ "$cur" = "$TARGET_SHA" ] || [ "$cur" = "$PATCHED_SHA" ]; then
    cp -f "$PATCHED" "$f"
    chmod 755 "$f"
  fi
done
