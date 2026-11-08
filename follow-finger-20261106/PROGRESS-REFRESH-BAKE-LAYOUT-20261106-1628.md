# PROGRESS — refresh bake layout (Asia/Hong_Kong 2026-11-06 16:28)

- my_product-bakein.img: BUILD-OK, **not flashable** (no my_product partition).
- Live: `/my_product` = folder on `system_a` (dm-2 ext4). Stock XML MD5 `7e48f867…`.
- Magisk v4d bind still active; proven MD5 `35db38f8…`.
- Next deploy: **live remount bake** via `display-refresh-system-v4/bake-in/live-bake-refresh-xml.sh` (see LAYOUT-AND-NEXT.md). No flash this step.
- hardware_success_claimed=false
