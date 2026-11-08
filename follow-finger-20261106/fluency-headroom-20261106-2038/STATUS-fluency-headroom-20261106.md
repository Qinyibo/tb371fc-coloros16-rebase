# STATUS — Fluency headroom scan (T2 accepted)

**Device:** TB371FC ColorOS16 OPD2413_16.0.10.600(CN01)
**Time:** 2026-11-06 ~20:42 Asia/Hong_Kong (UTC+8)
**hardware_success_claimed:** false
**Preserved:** Douyin `fullorientation` status=1 + magic=2 PAD exclude; SF T2 `mWorkDuration=6.94`; refresh bake; pen; luna path B; interconnect

## Closed / accepted (do not restack)

| Lever | Live evidence | Verdict |
|-------|---------------|---------|
| SF duration T2 | `mWorkDuration=6.94` `mReadyDuration=8.50`; SF activeMode **144.00 Hz** | **Accepted** — leave |
| System refresh bake | `defaultRateId=4-4-2-4` `maxrefreshsettings=4` `defaultMaxRate=144`; MD5 `35db38f8…`; `mCurrentPickRate=144`; `mCurrentPickMode=4`; `mPanelRateData=[4,4,2,4]` | **Accepted** |
| Dynframe 144 Magisk | Module present; live `sys_dynamic_frame_config.xml` MD5 `910955b1…` = **stock**; module copy `fb92391a…` not applied (prior ABA FAIL vs stock) | **Closed as FAIL** — do not re-enable |
| VRR touchidle-off module | Present / intended on | Keep; not re-tuned this turn |
| Luna heap path B | Module present | Keep |

Magisk inventory: `tb371fc_dynframe_144`, `tb371fc_luna_heap_offset_fix`, `tb371fc_sf_duration_144` (**disabled**), `tb371fc_sf_duration_donor_loose` (**enabled** → T2 path), `tb371fc_system_refresh_policy`, `tb371fc_vrr_touchidle_off`.

## Same-condition warm interrupt (this turn)

Protocol: force-stop → cold launch → settle 6s → `gfxinfo reset` → **12×** `input swipe` (80ms) → dump. Not identical to prior unlocked gfx journals; **no success claim**.

| App | Janky | p50 / p90 / p95 / p99 | Missed Vsync | High input latency | PickRate |
|-----|-------|------------------------|--------------|--------------------|----------|
| WeChat | 62/193 (**32.12%**) | 9 / 19 / 27 / 105 ms | 29 | 224 | 144 |
| Douyin | 28/192 (**14.58%**) | 5 / 15 / 25 / 81 ms | 5 | 187 | 144 |
| Luna | 69/411 (**16.79%**) | 8 / 23 / 32 / 101 ms | 41 | 658 | 144 |

Artifacts: `follow-finger-20261106\fluency-headroom-20261106-2038\gfx-*.txt`, `oplusscreenmode.txt`, `sf.txt`.

## Remaining headroom (product / ScreenMode / SF — not Magisk glue stack)

1. **Launcher 120 vs window 144 oscillation** — `oplusscreenmode` shows `PRIORITY_LAUNCHER_REQUEST` voting **120** while `PRIORITY_WINDOW_REQUEST` wants **144** (Launcher win preferred rateId=4 but launcher vote forces 120). Product/policy question: whether launcher idle vote should stay 120 or align with panel 144. **Evidence-only next ABA** if pursued.
2. **`appSwitchBoostType="0"`** in refresh_rate_config (`AppSwitchBoost=true`). Prior fluency notes flagged AppSwitchBoostType as a candidate; **not** stacked this turn — needs dedicated same-protocol ABA vs type≠0 without touching T2.
3. **`mReadyDuration=8.50` vs `mWorkDuration=6.94`** — ready budget still looser than work; further SF duration tightening already rejected path (T2 accepted). Treat as **closed for duration**, open only if donor shows different ready/work pairing **with** better warm evidence.
4. **High input latency counts** (esp. Luna 658) — points to **Input/NVT vs 144 vsync** path (prior follow-finger), not another rate-table Magisk. Next product-layer probe: touch sampling / InputDispatcher timing vs SF vsync — separate one-shot, no freq/whitelist.
5. **Dynframe** — already ABA FAIL; leave off.
6. **平行视界 UI richness** — **materials blocked** (see `landscape-parallel\MATERIALS-REQUEST-parallel-ui-20261106.md`); unrelated to fluency FPS.

## Recommended next deploy (if any)

**Do not** add Magisk modules on top of T2/refresh/dynframe/vrr stack.

Preferred single next experiment (optional):
- **A (fluency):** one-shot ABA on **Launcher 120 vote** or **appSwitchBoostType** change via **product `refresh_rate_config.xml` / ScreenMode policy** only — same warm-interrupt protocol as this folder — keep T2 6.94 unchanged.
- **B (UX):** wait for old-package FlexibleWindow/Settings materials before any 平行视界 UI deploy.

## Not claimed

hardware_success_claimed stays **false**. No fluency win declared from this scan.
## Update 2026-11-06 21:03 — ABA A/B completed

See `follow-finger-20261106\fluency-aba-A-launcher120-B-appswitch-20261106\STATUS-fluency-ABA-AB-20261106.md`.

- A launcher 120: **cause found, product fix blocked** (launcher APK hardcoded 120.0f). Left as-is.
- B appSwitchBoostType: **0→2 KEEP** (matched warm-switch ABA). Live MD5 `67a0e527…`.
- hardware_success_claimed=false.
