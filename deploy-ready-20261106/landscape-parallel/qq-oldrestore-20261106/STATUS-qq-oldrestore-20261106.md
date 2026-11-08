# STATUS — QQ dual restore from old package (2026-11-06 ~23:12 HKT)

**Device:** TB371FC ColorOS16 Qin HA1W0JA3  
**Package:** `com.tencent.mobileqq` 9.3.80  
**hardware_success_claimed:** false  

**KEEP verified:** SF T2 `debug.sf.early.app.duration=6944444` / `early.sf=8500000`; `appSwitchBoostType=2`; FWUI SHA256 `19D328584BB1E8AD2B677B9D06E2C492675E306FFB214B3022CADE48B00AF7E2`; no OEM spoof.

---

## User ask

旧包 QQ 双窗能用；现机只修了一部分。要求按旧可用包完整恢复长期双窗，不要 TIM/GuildBlank 半吊子。

## What old package actually had (evidence)

| Source | QQ magic |
|--|--|
| R94 / donor `sys_fantasy_window_managed*.xml` | **status=2** + `forceBlock:true` only (no activityPairs / mainPage / relatedPage) |
| Old live DB `WeChat-fantasywindow-readonly.db` (codex-20261028) | status=2, `excludeDevice:FOLD\|PAD`, forceBlock body, config len 758 |
| Old screenshots `mobileqq_native.png` / `mobileqq_460.png` / `qq_dpi320.png` | **QQ native pad UI**: left chat list + right empty QQ watermark — **not** oplus-magic-windows |

**Conclusion:** 旧包 QQ「双窗」= 平板原生分栏，不是平行视界 magic。产品表里 QQ 一直是 forceBlock。TIM 才有 Splash→* pairs。微信双窗靠 app TaskFragmentOrganizer + EmptyActivity，QQ 没有对等 EmptyActivity。

## Diff vs live v3 (before this restore)

| | v3 (half measure) | Old known-good (restored) |
|--|--|--|
| magic status | 1 | **2** |
| body | Splash pairs + Chat* + windowsRatio + scaleWindow=-1 | **forceBlock** thin Activities |
| config | invented TIM/WeChat-ish | **excludeDevice FOLD\|PAD** + fullscreen viewers |
| runtime mode | `oplus-magic-windows` centered single pane | target: no magic |

## Applied (product bake + runtime)

| Layer | Change |
|--|--|
| `/my_product/etc/fantasy/sys_fantasy_window_managed.xml` | QQ magic → old status=2 forceBlock row (MD5 `35dd71ab…`) |
| `/my_product/etc/fantasy/sys_full_orientation_managed.xml` | QQ FO **status=1** (old DB had FO=2; FO=1 kept so landscape works — SplashActivity is `SCREEN_ORIENTATION_PORTRAIT`) |
| `fantasywindow.db` | magic status=2 custom_mode=0 + old config/body; FO status=1 |

Artifacts: `landscape-parallel\qq-oldrestore-20261106\`  
Scripts: `scripts\apply-product.sh`, `apply-db.sh`, `apply-final.sh`

## Verify

- Task **mode=`fullscreen`**, bounds `0,0–2944,1840` — **not** `oplus-magic-windows`
- FO config present (`OplusFullOrientationAppConfig mStatus=1`)
- UI: landscape full-width message list (Pad login banner). **Not** old left|right empty watermark dual
- Opening chat stays in `SplashActivity` (9.3.80 AIO-in-Splash) — no second Activity for system split

## Honest limit (not half-glued further)

1. Restoring **full old fantasy policy** is done. That policy **never** enabled QQ magic dual.
2. Old visual dual = QQ **app-native pad layout**. Current 9.3.80 on this port does **not** draw that dual even with old fantasy restored.
3. Re-enabling GuildBlank `relatedPage` recreates stuck/unfocusable task — **do not**.
4. Long-term paths left (not done this turn): older QQ that still uses pad dual / ChatActivity; or QQ remote/in-app pad dual flag if found — **not** more magic invention.

## Classification

| Tag | |
|--|--|
| system/product policy | fantasy XML remount + DB sync to **old known-good** |
| intentional FO delta | FO=1 vs old FO=2 for landscape on this port |
| not glue | no Magisk bind, no OEM spoof, no GuildBlank |
| remaining gap | QQ 9.3.80 native pad dual UI absent |

## Rollback

Product bak on device: `/data/local/tmp/sys_fantasy_window_managed.pre-oldrestore-*.xml`, `sys_full_orientation_managed.pre-oldrestore-*.xml`  
DB bak: `/data/local/tmp/fantasywindow.pre-oldrestore.db`, `/sdcard/Download/fantasywindow.pre-oldrestore.db`  
Or re-apply prior v3 payloads under `qq-parallel-deep-20261106\`.