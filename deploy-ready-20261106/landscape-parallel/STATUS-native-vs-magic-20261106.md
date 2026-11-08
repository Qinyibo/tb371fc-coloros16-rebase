# STATUS — Douyin native landscape + 平行视界 deep dive

**Device:** TB371FC ColorOS16 (Qin) OPD2413_16.0.10.600(CN01)
**Time:** 2026-11-06 ~20:35 Asia/Hong_Kong (UTC+8)
**hardware_success_claimed:** false
**Untouched:** SF T2 (`mWorkDuration=6.94`), refresh bake, pen, luna path B, interconnect KEEP, Magisk modules besides fantasy DB

---

## User ask

1. Douyin after prior FantasyWindow patch is **not native landscape** — magic-window fake (portrait activity in pane). Want real native landscape.
2. 平行视界 UI vs older working package: current only shows rigid few modules.

---

## A) Native vs magic — evidence

### Magic (rejected prior patch)
- Task `mode=oplus-magic-windows`
- Activity config **`port`**, `requestedOrientation=PORTRAIT`
- Pane bounds e.g. `Rect(736,0-3089,2944)` (not full 2944×1840)
- Display `ROTATION_90` while activity rotation inside pane `ROTATION_0`

### Native (this fix)
- Task `mode=fullscreen`
- Activity **CurrentConfiguration / OverrideConfig: `land`**
- Bounds `Rect(0,0-2944,1840)` fullscreen
- Still `requestedOrientation=PORTRAIT` (app asks portrait) but **system delivers landscape config** via FullOrientation
- `OplusFullOrientationAppConfig{mPackageName=com.ss.android.ugc.aweme, mStatus=1, ...}`
- Screenshot: `probe/douyin-native-v2.png`

### Root cause of fake landscape
Prior patch set FantasyWindow **`magicwindow status=1`** (removed `excludeDevice:PAD`). That forces Magic Window dual/compact pane — **not** native rotate.

OEM stock (donor + live `/my_product/etc/fantasy/`):
| function | aweme status | meaning |
|----------|--------------|---------|
| magicwindow | **2** + often PAD exclude | Magic/平行窗 OFF on PAD |
| fullorientation | **2** + activity allowlist | Native FO OFF / restricted |
| compactwindow | **2** | Compact OFF |

Real lever = **`use_function=fullorientation`**, not magicwindow.

### Why status=1 alone was not enough
Keeping OEM `custom_config_body` with large `alwaysFullOrientActivities` left activity config **`port`** even with `mStatus=1`.

Working body (v2):
```json
{"rao":"true","rotate_cam":"false"}
```
+ `status=1`, and **magicwindow restored to status=2** + `excludeDevice:PAD`.

---

## B) Old vs new Fantasy / Flexible / COSA

| Asset | Live / donor | Notes |
|-------|--------------|-------|
| `sys_fantasy_window_managed.xml` | version **20260706**, ~1.38MB | Matches donor-tree-case |
| `sys_full_orientation_managed.xml` | version **20260422**, ~112KB | Matches donor |
| `sys_compact_window_managed.xml` | 20260422 | Matches donor |
| `OplusFlexibleWindowUI.apk` | **2.0.0** / 8391979 B | Same size as donor-tree |
| Runtime DB `fantasywindow.db` | prefs a=20260706 b=20260515 | Dual source; cloud may rewrite |
| COSA | game-oriented prefs | Not Douyin landscape path |
| `sys_flexiblewindow_policy_list.xml` | scenarios 1–3, ratios 16:9\|4:3, maxWinNum=2 | Float/flexible policy, not app-list UI |

Older public-source notes (`parallel-windows.md`) target **WeChat/B站 magicwindow scaleWindow=-1** dual-pane — that is Fantasy magic, separate from Douyin native FO.

---

## C) Trim packages

Still disabled (not parallel core): floatassistant, games, AI, engineer, etc.
**Enabled / kept:** `com.oplus.pscanvas`, `com.oplus.cosa`, `com.oplus.pantanal.ums`, `com.oplus.uiengine`, `com.oplus.uxdesign`, `com.oplus.appplatform`, `com.coloros.smartsidebar`.

No additional trim re-enable required for Douyin FO. `com.oplus.customize.coreapp` remains disabled (CustCore; not 平行视界 UI).

---

## D) Why 平行视界 looks like “few rigid modules”

`com.oplus.pscanvas` SettingActivity UI dump (live) texts are **only float-window tutorials**:
- 全屏切换到浮窗 / 浮窗模式 / 手势模式 / 操作教程 / 交换应用 / 透明度调节 / 浮窗跳转 / 自由浮窗

OperationActivity: 快速上滑关闭…
SupportGameListActivity: 未发现已安装支持游戏

This is ColorOS16 FlexibleWindowUI **2.0.0 float/zoom settings**, not the older rich per-app parallel-layout console.

Also: Fantasy `magicwindow` rows with `installed=1` on this device = **only 5 packages** (mm, aweme, luna, oneplus.bbs, qq). Sparse installed set ⇒ even a full app list would look thin.

**Blocked for “old richness” without OEM UI pieces:** no alternate older FlexibleWindowUI found under `D:\TB371FC-release` beyond current donor 2.0.0; restoring classic parallel settings UI needs a different APK/settings fragment from an older port or Settings overlay — **not** fixed by re-enabling trim packages.

WeChat dual-pane magic (status=1) still available at Fantasy runtime if user wants 平行窗 for WeChat; Douyin intentionally left magic OFF.

---

## E) Fix applied (reversible)

1. Backup: `probe/fantasywindow.before-native-20261106.db`, stock `probe/fantasywindow.db.bak`
2. Deploy `probe/fw-native-douyin-v2.db` via `su -t $(pidof com.oplus.exsystemservice)`
3. Aweme rows now:
   - magicwindow **status=2** `config={"mode":"1","excludeDevice":"PAD"}`
   - fullorientation **status=1** `config/body={"rao":"true","rotate_cam":"false"}`
   - compactwindow status=2 unchanged
4. Kill exsystemservice → respawn; force-stop/relaunch Douyin
5. Verified fullscreen + `land` + full bounds; SF T2 still 6.94

### Scripts
- `redeploy-douyin-native.cmd` — push v2 DB again
- `rollback-douyin-native.cmd` — restore `fantasywindow.db.bak`

### Cloud risk
Fantasy ROM-update / cloud may rewrite `t_config`. If Douyin reverts, re-run redeploy or bake Magisk `/my_product/etc/fantasy/sys_full_orientation_managed.xml` overlay (next deploy; not done this turn).

---

## Next deploy steps

1. User visual confirm Douyin feed/video native landscape (not letterbox phone UI).
2. If cloud resets FO: Magisk product bind-mount patched `sys_full_orientation_managed.xml` (aweme status=1 + simple rao body) — preferred persistence vs data DB.
3. 平行视界 UI richness: hunt older FlexibleWindowUI / Settings parallel fragments from prior R94 user package **outside** current donor; do **not** re-enable floatassistant as substitute.
4. Optional: enable `fullorientation` similarly for other portrait-locked apps user names (same pattern).
5. Keep WeChat magicwindow status=1 if dual-pane still desired (separate from Douyin).

## Not claimed
- hardware_success_claimed = **false**
- Did not claim full restoration of old 平行视界 settings richness
- Did not stack ART/GC/OEM-identity/freq/whitelist