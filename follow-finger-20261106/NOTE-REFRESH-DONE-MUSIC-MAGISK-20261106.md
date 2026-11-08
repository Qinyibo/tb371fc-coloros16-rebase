---

## 2026-11-06 note (refresh bake + music Magisk packaging)

- Refresh XML live-bake into system `/my_product` is **done**; refresh Magisk disabled; ABA without bind still Version `20260107` / Preferred `[4,4,2,4]` for WeChat/Douyin/Luna.
- Music path B live so already applied (`2dc3bda3…`). Magisk module `tb371fc_luna_heap_offset_fix` had **Windows backslash filenames**, so `post-fs-data.sh` could not re-apply after app update — that packaging bug was the durability blocker. On-device layout repaired to Unix `lib/libsysoptimizer.so`; clean zip: `deploy-ready-20261106/music/tb371fc_luna_heap_offset_fix-v1-pathB-fixed.zip`.
- Soft check: no new HeapTaskDaemon tombstone. `hardware_success_claimed=false`. Next: pen V4 flash acceptance (`pen/DEPLOY.md`).