# ROM bake-in — refresh_rate_config.xml (TB371FC ColorOS16)

## Status (2026-11-06)
- Magisk ABA **PASS** (XML-only bind). See `../BAKE-IN-ABA-PASS.md`.
- This file is the **canonical** product config to bake into `my_product/etc/refresh_rate_config.xml`.
- After image bake + flash verified: **remove** Magisk module `tb371fc_system_refresh_policy`.
- `hardware_success_claimed=false` until ROM image path is flashed and ABA-repeated without Magisk.

## Why this file (not framework jar)
- `mPanelRateData.PreferredRefreshRateId` comes from
  `<item package="com.android.systemui" … rateId="4-4-2-4">`
  (or `activity="NotificationShade_controlPanel"`), **not** from `<config>`.
- `getSettingModeIndex` clamps setting mode 4 → index 3 → last tuple slot must be **4**.
- `defaultRateId` must be hyphen tuple `4-4-2-4` (scalar `"4"` → `[4,0,0,0]`).
- Magisk bind of `oplus-services.jar` **bootloops** — never bake a Magisk jar overlay for this.
- Product high-tier remap: item rateId A/D components `3→4` (1001 items) so WeChat/Douyin/Luna PickRate=144 without per-app Magisk glue modules.

## Image build step (Codex / ROM)
1. Replace stock `my_product/etc/refresh_rate_config.xml` with this directory's `refresh_rate_config.xml` (UTF-8 **no BOM**).
2. Confirm MD5 of baked file == Magisk-proven `35db38f8c85758c372546c707513642c` (or re-hash after any intentional edit).
3. Flash → reboot → ABA checklist below **with Magisk module disabled/removed**.
4. Keep `tb371fc_luna_heap_offset_fix` independent (music); do not fold into this refresh module.

## ABA checklist (post ROM bake, no Magisk refresh module)
- `dumpsys oplusscreenmode` → `Version:20260107`
- `mDefaultRateId=[4, 4, 2, 4]`
- `PreferredRefreshRateId=[4, 4, 2, 4]`
- `control panel:4`
- Warm start WeChat / Douyin / Luna → `mCurrentPickRate=144`
- SF vs panel: expect 144 when PickRate=144

## Related
- Reverse: `../RATE-TABLE-REVERSE.md`
- Magisk trial: `../product-config/magisk-module/`
- Pass log: `../BAKE-IN-ABA-PASS.md`
