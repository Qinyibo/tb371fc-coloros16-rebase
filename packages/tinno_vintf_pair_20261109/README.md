# tb371fc_tinno_vintf_pair — Magisk systemless VINTF pair fix

## What this does
Pairs the Tinno keyboard VINTF names that currently disagree on ColorOS port `OPD2413_16.0.0.210` + `boot-r108-resx`:

| Path | Before | After (overlay) |
|------|--------|-----------------|
| `/vendor/etc/vintf/compatibility_matrix.xml` | `vendor.mediatek.hardware.tinno_keyboard` (optional) | `vendor.qti.hardware.tinno_keyboard` (optional kept) |
| `/vendor/etc/vintf/manifest/vendor.qti.hardware.tinno_keyboard@1.0-service.xml` | missing | declares HIDL `ITinnoKeyBoard/default` |

Live HAL binary/rc already use `vendor.qti.hardware.tinno_keyboard@1.0`. This module does **not** remount or write the vendor partition.

## Magisk mount layout (30.7)
Files live under `system/vendor/...` inside the module zip. Magisk 24+ mounts `/system/vendor` onto the real `/vendor` partition via bind overlays. We intentionally do **not** use a top-level `vendor/` folder; `system/vendor/` is the documented Magisk norm for separate-vendor devices.

## Install (after Magisk boot is flashed by operator)
1. Flash `boot-r108-resx-magisk.img` to `boot_a` only when instructed (see `flash-install.ps1` / `flash-install.sh`). Keep stock `boot-r108-resx.img` as rollback.
2. Boot, complete Magisk first-run / grant if needed.
3. `adb push tb371fc_tinno_vintf_pair.zip /data/local/tmp/`
4. `adb shell su -c 'magisk --install-module /data/local/tmp/tb371fc_tinno_vintf_pair.zip'`
5. One reboot.
6. Verify:
   - `getprop init.svc.tinnokeyboard` (hope `running`; oneshot may still show `stopped` after exit — also check logcat / hwservicemanager)
   - `grep tinno /vendor/etc/vintf/compatibility_matrix.xml` should show `qti` via Magisk mount
   - `ls /vendor/etc/vintf/manifest/*tinno*` should list the fragment

## Uninstall / rollback
- Disable or remove module: Magisk app → Modules → remove `TB371FC Tinno Keyboard VINTF Pair`, reboot.
  Or: `adb shell su -c 'rm -rf /data/adb/modules/tb371fc_tinno_vintf_pair'` then reboot.
- Full Magisk removal / return to stock boot: `fastboot flash boot_a E:\youxikaifa\work\today-20261109\boot-r108-resx.img` (sha `f5f44604…`), `fastboot set_active a`, reboot. Vendor partition was never modified.

## Hard rules preserved
- No `mount -o remount,rw /vendor`
- No verity/vbmeta disable (patched boot built with `KEEPVERITY=true`, `PATCHVBMETAFLAG=false`)
- No KEEP/gold vendor mix
- Keyboard stays unplugged until verify passes