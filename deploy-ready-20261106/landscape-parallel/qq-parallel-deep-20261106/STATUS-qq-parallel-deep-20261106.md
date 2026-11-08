# STATUS — QQ parallel deep dig (2026-11-06 ~22:50 HKT)

**Device:** TB371FC ColorOS16 Qin HA1W0JA3  
**Package:** `com.tencent.mobileqq` 9.3.80  
**hardware_success_claimed:** false  

**KEEP:** SF T2; 144; `appSwitchBoostType=2`; FWUI `19D32858…`; FO bulk for non-magic; **no OEM spoof**.

---

## User: QQ 双窗还是不行

### WeChat (works) vs QQ (broken) — runtime truth

| | WeChat `com.tencent.mm` | QQ `com.tencent.mobileqq` |
|--|--|--|
| Task windowing | `fullscreen` + **app** `TaskFragmentOrganizer` (`organizerProc=com.tencent.mm`) adjacent `multi-window` | system `oplus-magic-windows` |
| Dual evidence | `LauncherUI` + `EmptyActivity` right pane bounds e.g. `883–2944` | needs system `relatedPage` stub |
| Runtime magic `config` | **8275 B** cloud/server merge: `activityPairs` LauncherUI→* **and** `mainPage/relatedPage=EmptyActivity`, `supportAppTaskSplitScreen=true`, rich `UX.windowsRatio` | stock was **`{"mode":"1"}`**; R94 product even **status=2 + forceBlock** |
| Chat navigation | separate activities (`ChattingUI` etc.) | **9.3.80 keeps AIO inside `SplashActivity`**; `ChatActivity` / `AIOLocalActivity` exist but **not exported** — adb cannot start; normal tap does not spawn second Activity |

### What we tried

1. **v1 TIM Splash→*** + `scaleWindow=-1` — task enters magic, **no left–right dual** (single Splash).  
2. **v2 WeChat-aligned** `mainPage=Splash` + `relatedPage=GuildBlankActivity` + `supportAppTaskSplitScreen` — **WM dual formed** (Splash `0–1036` + GuildBlank `1038–2944`, `sz=2`, AdjacentSet). **But task stuck `visible=false` / unfocusable** (Launcher kept top). GuildBlank is not WeChat `EmptyActivity`; unusable. **Rolled forward to v3.**  
3. **v3 (current)** — drop `relatedPage` / `supportAppTaskSplitScreen` / `changeToFullscreen`; keep real Chat* pairs + PAD `windowsRatio` + `scaleWindow=-1`. **QQ opens and stays resumed** in `oplus-magic-windows` (centered magic pane `~736–2207`). Still **not** WeChat-style dual when opening a chat, because no second Activity is launched.

### Product / runtime now

| Layer | Path | State |
|-------|------|--------|
| Product | `/my_product/etc/fantasy/sys_fantasy_window_managed.xml` | MD5 `4a316e03…` (v3) |
| Runtime DB | `fantasywindow.db` magic row | config len **1664**, status=1 |
| Bak | `/data/local/tmp/sys_fantasy_window_managed.pre-qqv3-*.xml`, `pre-qqv2-*.xml`; `/sdcard/Download/fantasywindow.pre-qqv3.db` |

Artifacts: `qq-parallel-deep-20261106\` (payload v2/v3, verify dumps, `STATUS`).

### Classification

| Tag | Meaning |
|-----|---------|
| system/product policy | fantasy XML remount + DB sync |
| not glue | no Magisk / identity spoof |
| hard limit (this port + QQ 9.3.80) | WeChat dual needs **app-owned** split **or** a **true EmptyActivity-class** relatedPage; QQ has neither usable here. Stock OPPO **forceBlock**’d QQ. |
| next (if ever) | find inert QQ relatedPage that stays focusable; or older QQ that still starts `ChatActivity` for AIO; or accept FO fullscreen land instead of magic. **Do not re-enable GuildBlank relatedPage.** |

### User check

1. Open QQ — should show (centered magic / parallel shell), not stuck on launcher.  
2. Open a conversation — expect **single** pane content (not WeChat L/R) until a real second Activity appears.  
3. WeChat remains the reference for working dual.

