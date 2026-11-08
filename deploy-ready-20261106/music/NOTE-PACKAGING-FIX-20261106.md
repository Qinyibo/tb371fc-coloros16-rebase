# Music Magisk packaging fix — 2026-11-06

Refresh bake is done (system `/my_product` XML; refresh Magisk off).

Blocker for path-B durability across Luna updates was Magisk zip/layout using literal `\` names so `$MODDIR/lib/libsysoptimizer.so` was missing. Fixed on device; reinstall zip: `tb371fc_luna_heap_offset_fix-v1-pathB-fixed.zip` (Python zipfile, Unix paths, sha `2dc3bda3…`).

See `STATUS-20261106.md`. `hardware_success_claimed=false`.