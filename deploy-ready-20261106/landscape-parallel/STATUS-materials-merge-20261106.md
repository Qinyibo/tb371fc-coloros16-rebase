# STATUS — Materials merge: FlexibleWindowUI + ParallelWorld UI (2026-11-06 ~22:30 HKT)

**Device:** TB371FC ColorOS16 Qin HA1W0JA3  
**hardware_success_claimed:** false  
**KEEP untouched:** SF T2 `mWorkDuration=6.94` / `mReadyDuration=8.50`; refresh 144; `appSwitchBoostType=2`; pen; luna path B; interconnect; no OEM identity spoof

---

## Classification

| Item | Class | Action |
|------|-------|--------|
| Live Settings 16.1.0 `ParallelWorldFragment` | **system already present** | **KEEP** — per-app 平行视窗 list already works |
| Old Settings.apk 16.0.0 (materials) | **REJECT full replace** | Downgrade 16.1.0→16.0.0; system_ext only ~51M free; live already has richer ParallelWorld resources |
| Old OplusFlexibleWindowUI.apk SHA `19D32858…` | **system_ext remount bake** (`su -mm`) | **APPLIED** (float/zoom shell; does NOT host per-app list) |
| Fantasy DB magic/FO coexistence | **product + runtime** (prior parallel-restore) | Magic apps: magic=1 + FO=2; non-magic: FO bulk=1 |
| Magisk Settings/FWUI module | not used | remount succeeded for FWUI |
| OEM identity spoof | rejected | — |

---

## What user was missing

Opening **pscanvas** `SettingActivity` (浮窗教程) ≠ **Settings** `ParallelWorldFragment` (逐应用开关).  
Live Settings already had the list; materials Settings was not required to “unlock” it.

**Open list:** run `landscape-parallel\open-parallel-world.cmd`  
Or Settings search **平行视窗**.

Verified UI titles (all switches on): OPPO视频, QQ, 抖音, 浏览器, 媒体播放器, 汽水音乐, 微信, 文档, 相册, 一加社区, 音乐, 阅读.

---

## FlexibleWindowUI remount

| | SHA256 | size |
|--|--------|------|
| Pre (live) | `01450E66939EAC2A0E188396244B1F59725E862342BE978CA60CD8E218BE7BB8` | 8391979 |
| Post (materials R94) | `19D328584BB1E8AD2B677B9D06E2C492675E306FFB214B3022CADE48B00AF7E2` | 7600418 |
| Path | `/system_ext/app/OplusFlexibleWindowUI/` + matching `oat/arm64/*.vdex` | |

Apply: `fwui-remount-20261106\apply-fwui.cmd`  
Rollback: `fwui-remount-20261106\rollback-fwui.cmd`  
On-device bak: `/data/local/tmp/fwui-bak-20261106/`

Note: class surface ≈ live (SettingActivity / SupportGameList / float guide). **Per-app parallel list remains in Settings**, not FWUI. Remount satisfies materials hash parity; list UX was Settings-side.

Plain `mount -o remount` fails on dm-3; need **`su -mm`**.

---

## Settings.apk — REJECT evidence

1. Live versionName **16.1.0** / versionCode 16001000 vs materials **16.0.0** / 16000000  
2. Live DEX already contains `ParallelWorldFragment` + `loadAppList` + `parallel_world_preference.xml`  
3. Live UI dump proves 12-app list with switches  
4. system_ext free ~51M; Settings ~185–188MB — unsafe in-place swap without delete-first  
5. Risk: ColorOS Settings priv-app tightly coupled to framework 16.1

---

## Coexistence policy (FO + 平行视界)

| App class | magicwindow | fullorientation | User effect |
|-----------|-------------|-----------------|-------------|
| Parallel-capable installed (12) | status=1, installed=1 | status=**2** (demoted so magic wins) | Toggle ON in 平行视窗 → dual/magic; FO not forced fullscreen |
| Other apps (FO bulk) | none / N/A | status=**1** rao:true | Native fullscreen landscape |
| Toggle OFF parallel for an app | Settings updates magic status via FoldClient | FO stays 2 for that package | May lose dual-pane; not auto-promoted to FO=1 (OEM semantics) |

Do **not** set FO=1 on magic apps again — that overrides dual-window (prior bulk mistake).

---

## Smoke (landscape forced)

| App | Task mode |
|-----|-----------|
| 抖音 | **oplus-magic-windows** + TaskFragment |
| QQ | **oplus-magic-windows** |
| 汽水 | **oplus-magic-windows** |
| 微信 | LauncherUI **fullscreen land**; open a chat for dual-pane (activityPairs) |

---

## Materials dir

`materials-from-old-package\` (MANIFEST.md) — Settings kept as reference only; FWUI+vdex consumed.

## Out of scope / not done

- Settings.apk Magisk overlay / full replace  
- Seeding magic rows for calculator/alarm/etc. (no product XML rules)  
- Bilibili (not installed on this device now)  
- hardware_success_claimed remains **false**