# FLASH-VENDOR-DONOR-LOOSE-RESULT

**时间:** 2026-11-06 Asia/Hong_Kong (~18:22–18:25)
**hardware_success_claimed=false**

## Outcome (priority: device healthy)

| Item | Result |
|------|--------|
| Patched vendor fully flashed? | **NO** — never completed |
| Rollback flash used? | **NO** — not needed; original vendor data intact |
| Boot after failed attempt | **OK** via `fastboot reboot` from fastbootd |
| `sys.boot_completed` | `1` |
| slot | `_a` |
| `mWorkDuration` | **8.89** (unchanged stock baseline) |
| `mReadyDuration` | 10.94 |
| refresh XML MD5 | `35db38f8c85758c372546c707513642c` preserved |
| Display | renderFrameRate 144, defaultModeId 2 |
| Luna Magisk | kept (no `disable`) |
| SF duration Magisk modules | still `disable`d |

## What was attempted

1. Pre-checks OK: dump SHA `DE93DE50…`, patched SHA `6e52ab82…`, live healthy 8.89 / refresh 35db38f8 / SF Magisk disabled.
2. Bootloader (`is-userspace=no`, `product=spinel`) has **no** `vendor_a` getvar — LP only in fastbootd.
3. Entered fastbootd (`product=TB371FC`, `is-userspace=yes`, `is-logical:vendor_a=yes`, size `0x35A0F000` = 899739648 = image size).
4. `fastboot flash vendor_a vendor_a-LIVE-sf-donor-loose.img` → `Resizing OKAY`, then **FAILED** `AdbWriteEndpointSync` semaphore timeout (121) on first sparse chunk; also warned `Invalid sparse file format at header magic` (raw img).
5. Multiple rollback attempts of `vendor_a-LIVE-dump.img` with `-S 128M/32M/8M` — **all failed same USB write timeout** before any successful chunk.
6. Rescue: `fastboot reboot` → Android returned ~20s later with stock vendor props (`high_fps_*` present, no duration props).

## Conclusion

- **flashed patched: no**
- **boot: ok**
- **rollback flash: not used** (data never replaced)
- **new mWorkDuration: none** (still 8.89)
- Fastbootd large `vendor_a` raw writes currently unreliable on this host USB path; do not retry until true sparse (`img2simg`) and/or bootloader-side super rewrite path is ready.
- Pen V4 / refresh / luna: preserved.

## Paths

- Prep: `D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\sf-duration-vendor-bake\vendor-offline-prep\`
- Dump (rollback): `vendor_a-LIVE-dump.img`
- Patched (unflashed): `vendor_a-LIVE-sf-donor-loose.img`
- This doc: `D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\sf-duration-vendor-bake\FLASH-VENDOR-DONOR-LOOSE-RESULT.md`
- Pre-flash note: `...\sf-duration-vendor-bake\PRE-FLASH-VENDOR-DONOR-LOOSE.md`
