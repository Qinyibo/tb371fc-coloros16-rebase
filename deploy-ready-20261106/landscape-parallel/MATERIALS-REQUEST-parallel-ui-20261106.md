# MATERIALS REQUEST — 平行视界 richer UI (ONE shot)

**Time:** 2026-11-06 ~20:42 Asia/Hong_Kong (UTC+8)
**hardware_success_claimed:** false
**Blocked deploy:** restoring old fuller 平行视界 console (per-app list / layout modes), not ColorOS16 float-tutorial UI

## Why blocked

Live and donor are the **same** OEM piece:

| Item | Value |
|------|-------|
| Package | `com.oplus.pscanvas` / `OplusFlexibleWindowUI.apk` |
| versionName | 2.0.0 (versionCode 20) |
| Size | 8391979 |
| SHA256 | `01450E66939EAC2A0E188396244B1F59725E862342BE978CA60CD8E218BE7BB8` |
| Live path | `/system_ext/app/OplusFlexibleWindowUI/OplusFlexibleWindowUI.apk` |
| Donor path | `donor-tree\system_ext\app\OplusFlexibleWindowUI\OplusFlexibleWindowUI.apk` |

UI dump of SettingActivity is only float tutorials (全屏切浮窗 / 手势 / 交换 / 透明度 / 自由浮窗). OperationActivity / SupportGameListActivity likewise thin.

## Searched on D: (no alternate older FlexibleWindowUI)

- `clean-rebase-20261104\donor-tree` / `donor-images` → same 2.0.0
- `deploy-ready\...\probe\OplusFlexibleWindowUI.apk` → same hash
- `v23-test-apks` → only aweme/mm/qq/bili trees
- R94 flash trees (v23/v27/OCT18/v22a) → `images\super-R94.img` (+ boot/vbmeta); **no extracted** `OplusFlexibleWindowUI` at shallow depth; not a separate older APK
- `original\OPD2413_16.0.10.600_CN01.zip` → 7z `*FlexibleWindow*` = **0 files** (packed inside super/payload)
- `public-source\TB371FC-ColorOS16` → docs/patches for WeChat/B站 **magicwindow rules**, not a richer Settings/FlexibleWindow UI APK

Trim re-enable cannot restore UI richness; frameworks already match donor.

## Exact materials needed (provide any ONE of these)

1. **Older working package dump** from the build where 平行视界 had full app-list / layout modules:
   - `system_ext/app/OplusFlexibleWindowUI/OplusFlexibleWindowUI.apk` (+ oat if present)
   - AND/OR Settings fragments that hosted parallel UI (`Settings.apk` / `OplusSettings*.apk` / overlay APKs that contain 平行视界 preference XML)
2. Or an **extracted `system_ext` tree / `system_ext.img`** from that older R94 working flash where FlexibleWindowUI SHA256 **≠** `01450E66…`
3. Optional but useful: screenshot or UI hierarchy of the old 平行视界 settings page (to know which activities/preferences to restore)

Place under e.g.  
`D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\materials-from-old-package\`

## After materials arrive

Diff APK/resources vs live 2.0.0 → minimal Magisk `system_ext` replace or remount bake → verify SettingActivity texts include per-app parallel list / ratio modes → keep Douyin `fullorientation` and T2 untouched.

## Do not ask again until materials land

This is the single materials request for the 平行视界 UI gap.

## Update 2026-11-06 22:05
Bulk FO + fantasy product adaptation applied (STATUS-bulk-fo-parallel-20261106.md). UI APK MATERIALS still required for rich parallel settings shell; backend magic allowlist already ~2887 enabled + 7 installed gaps added. Do not re-request piecemeal.
