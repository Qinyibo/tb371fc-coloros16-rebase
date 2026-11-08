#!/system/bin/sh
MODDIR=${0%/*}
# Accept original, pathA (0x308), or pathB (disable-apply)
ORIG=e8357c10cef28edb36ad59faeec51d120c9ae41f04ff3de8f5874349dc5f7ec3
PATHA=be0565463b741685bdf95803fbb9d5de57832ad862b5e66555df2df7ecc66416
PATHB=2dc3bda37442e36f9fd6d3b2a19aec427e59c0393449f0ffb433095c94cf0b4e
PATCHED="$MODDIR/lib/libsysoptimizer.so"
[ -f "$PATCHED" ] || exit 0
for f in /data/app/*/com.luna.music*/lib/arm64/libsysoptimizer.so /data/app/*/*/lib/arm64/libsysoptimizer.so; do
  [ -f "$f" ] || continue
  # only touch luna paths
  echo "$f" | grep -q com.luna.music || continue
  cur=$(sha256sum "$f" | cut -d' ' -f1)
  if [ "$cur" = "$ORIG" ] || [ "$cur" = "$PATHA" ] || [ "$cur" = "$PATHB" ]; then
    cp -f "$PATCHED" "$f"
    chmod 755 "$f"
  fi
done
