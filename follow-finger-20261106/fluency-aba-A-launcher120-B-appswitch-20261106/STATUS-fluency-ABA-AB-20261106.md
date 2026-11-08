# STATUS — Fluency ABA A (launcher 120) + B (appSwitchBoostType)

**Device:** TB371FC ColorOS16 OPD2413_16.0.10.600(CN01) HA1W0JA3
**Time:** 2026-11-06 21:03 Asia/Hong_Kong (UTC+8)
**hardware_success_claimed:** false
**Folder:** `follow-finger-20261106\fluency-aba-A-launcher120-B-appswitch-20261106`

## Preserved (verified live after KEEP)

| Item | Live |
|------|------|
| SF T2 | `mWorkDuration=6.94` `mReadyDuration=8.50` activeMode 144 Hz |
| Refresh bake base | `defaultRateId=[4,4,2,4]` `mCurrentPickRate=144` |
| appSwitchBoostType | **2** (KEPT) — XML MD5 `67a0e527351ae50bcd5a23ff542164ff` |
| Pen / luna path B / interconnect / Douyin fullorientation | untouched this turn |
| Magisk glue | **not** used (live remount of product XML only) |

---

## ABA A — Launcher 120 vs window 144 oscillation

### Cause (code-backed)

1. Product `<item package="com.android.launcher" rateId="4-2-2-4"/>` already drives **PRIORITY_WINDOW_REQUEST = 144** (preferred rateId=4 when setting mode clamps to index 3).
2. Intermittent **PRIORITY_LAUNCHER_REQUEST (priority=85)** votes **120.0 Hz** and wins over WINDOW (0) because 85 > 0.
3. Source: `OplusLauncher` `LauncherBooster$CpuBoost.requestRefreshRateByInvoke` reflects into `OplusDisplayModeManager.requestRefreshRate(priority=85, status, **Float 0x42f00000 = 120.0f**, bundle)`.
4. Hardcoded **120.0f** in launcher APK — not derived from `refresh_rate_config.xml` rateId table.
5. Steady-state home dumpsys often shows only WINDOW 144; 120 appears during launcher gesture/animation boost windows (back/swipe-to-home etc.).

### Product-layer trial

**None applied.** No product XML single-variable change can override the hardcoded 120.0f without patching `OplusLauncher.apk` (forbidden this turn: no Magisk/APK glue stack).

### Verdict A

| Result | **MATERIALS/CODE BLOCKED for product-only fix** |
|--------|--------------------------------------------------|
| Kept | stock launcher vote behavior (hardcoded 120 during anim) |
| Reverted | n/a (no trial write) |
| Next if pursued | launcher APK binary patch of 120.0f→144.0f (out of scope here) or OEM ScreenMode remap of priority 85 |

Artifacts: `A-launcher120/` (cause notes via parent folder scripts), booster decompile under `fluency-aba-launcher144-20261106\L-requestRefreshRateByInvoke.txt`.

---

## ABA B — appSwitchBoostType 0 → 2

### Cause

`enableAppSwitchBoost=true` but `appSwitchBoostType="0"` → `notifyActivityResume` hits:

> `app switch boost type is 0, disable app switch boost.`

Type semantics (from `OplusRefreshRatePolicyImpl$LocalService.notifyActivityResume`):

| Type | Behavior |
|------|----------|
| 0 | **Disable** boost |
| 1 | Boost only when same-package switch |
| ≠0 and ≠1 (e.g. **2**) | Boost on cross-app switches (needed for WeChat↔Douyin↔Luna) |

`startAppSwitchBoost` then votes `PRIORITY_START_ANIMATION_BOOST` at `boostId=4` (144 Hz) for ~2s.

### Protocol (matched A/B)

- No force-stop / not COLD.
- Open WeChat, Douyin, Luna; warm `am start` switches between already-open apps; `gfxinfo reset`; 12× `input swipe` 80ms; dump.
- Single variable: `appSwitchBoostType` only (remount `/my_product/etc/refresh_rate_config.xml` on system_a).

### Results (same-condition warm switch)

| App | B0 type=0 janky / p90 | B1 type=2 janky / p90 | Delta |
|-----|------------------------|------------------------|-------|
| WeChat | 15.60% / 22 ms | 19.24% / **15 ms** | janky% +noise; p90 better |
| Douyin | 37.93% / **150 ms** | **25.97% / 40 ms** | clear win |
| Luna | 52.87% / **121 ms** | **14.89% / 18 ms** | clear win |

Boost log B1: `Trigger app switch boost … boostId=4` + `PRIORITY_START_ANIMATION_BOOST → 144`.
Boost log B0: `don't do app switch boost` / no Trigger lines.

### Verdict B

| Result | **KEEP type=2** |
|--------|-----------------|
| Live XML MD5 | `67a0e527351ae50bcd5a23ff542164ff` (was `35db38f8…`) |
| Rollback | `B-appswitch\refresh_rate_config.pre-B1.xml` (MD5 `35db38f8…`) + `revert-B0.sh` remount pattern |

---

## One-shot conclusion

1. **Launcher 120 oscillation:** root-caused to OplusLauncher hardcoded 120.0f at PRIORITY_LAUNCHER_REQUEST; **not** product-rateId fixable; **left as-is**.
2. **appSwitchBoostType:** 0 was disabling the OEM app-switch 144 boost; **type=2 KEPT** after matched warm-switch ABA (Douyin/Luna large wins; WeChat p90 improved).
3. T2 6.94 + refresh 144 panel policy + pen/luna B/interconnect untouched.
4. **hardware_success_claimed=false** (no subjective user sign-off claimed).
5. Parallel FlexibleWindow UI remains **MATERIALS-BLOCKED** (not pursued).

## Rollback (type=2 → 0)

```
adb push ...\B-appswitch\refresh_rate_config.pre-B1.xml /data/local/tmp/refresh_rate_config.pre-B1.xml
adb shell su -mm -c 'sh /data/local/tmp/revert-B0.sh'   # or apply-keep with pre-B1 as SRC
adb reboot
```