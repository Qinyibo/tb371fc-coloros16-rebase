# STATUS — Blackscreen cannot wake (2026-11-06 ~22:36–22:40 HKT)

**Device:** TB371FC ColorOS16 Qin HA1W0JA3  
**hardware_success_claimed:** false  
**KEEP after recovery:** SF T2 `mWorkDuration=6.94` / `mReadyDuration=8.50`; 144 Hz; `appSwitchBoostType=2`; FWUI SHA `19D32858…` (not rolled back); fantasy FO/magic product tables (not rolled back)

---

## User question

**是不是因为修平行视窗导致的？**

### Verdict: **No**

Proximate cause is **kernel panel unblank failure**, not FWUI remount / fantasy magic-QQ / parallel-restore product or DB edits.

| Suspect (today) | Link to blackscreen? | Evidence |
|-----------------|----------------------|----------|
| FWUI remount `19D32858…` (~22:28) | **No** | Userspace `system_ext` APK only; no DRM/DSI touch; still installed after successful recovery |
| Fantasy parallel-restore / FO bulk (~22:03–22:23) | **No** | XML/DB under `/my_product/etc/fantasy` + `fantasywindow.db`; no panel driver path |
| QQ magic pairs bake (~22:34) | **No (not proximate)** | Same fantasy layer; no FATAL/`am_crash` for `mobileqq` / `pscanvas` / `exsystemservice` in ring; recovery succeeded **without** QQ DB/XML rollback |
| SF T2 / refresh 144 / type=2 | **No (unrelated this incident)** | Baked earlier; still healthy post-reboot (`vsyncRate=144`, T2 durations intact); not changed at ~22:34 |
| Panel R107/R94 path | **Yes — proximate** | See dmesg below |

**Temporal note (not causation):** User was validating QQ 平行视窗 ~2 minutes before report; rapid sleep/wake (power key + ADB) can stress panel resume. That is session trigger context, not proof that fantasy config corrupted the display stack.

---

## Proximate cause (evidence)

Pre-reboot dumpsys:

- ADB online; `mWakefulness=Asleep` then after `svc power stayon` → `Awake`
- `mScreenState=ON` but **`mBrightness=0.0`** while compositor still had frames (`blackscreen-probe.png` ~4.3 MB; focus `NotificationShade` over `com.tencent.mobileqq/.activity.SplashActivity`)
- Framework believed display on; user saw black → panel not lighting

Pre-reboot dmesg (saved `dmesg-r107-pre-reboot.txt`), repeated on wake:

```
R104_PANEL_DEAD_POWER_ON allowing existing rail recovery
R94_PANEL_POST_ARMED waiting_native_commit_completion
R94_NATIVE_COMPLETE_REK_FAILED -1 IRQ_CLOSED_DISPLAY_RETAINED
R107_NATIVE_UNBLANK_FAILED rc=-1 conn_id=29
```

Logcat ring: normal `goToSleepFromPowerButton` / `OplusBlackScreenGestureControllExImpl` / short `ScreenOnUnblocker` (~38–40 ms). **No** FlexibleWindow/FWUI/fantasy FATAL tying to blank.

---

## Recovery (done)

1. Soft wake (`stayon` / KEYCODE_WAKEUP) → framework Awake but panel still R107-stuck  
2. **`adb reboot`** (~22:38 HKT)  
3. Post-boot: `boot_completed=1`, `Awake`, `mScreenState=ON`, **no new R107/R94_NATIVE_COMPLETE failures** in dmesg (only false-positive match on kernel build tag `r107-clean-erofs`)  
4. Brightness: device min is `mScreenBrightnessRangeMinimum=222`; raised via `su settings put system screen_brightness 3500` → `Display Brightness≈917`  
5. **Did not** rollback FWUI / fantasy QQ / FO bulk / T2 / refresh  

Artifacts:

- `logcat-ring-20261106-223643.txt`, `logcat-full-diag.txt`, `crash-ring.txt`
- `dmesg-r107-pre-reboot.txt`
- `blackscreen-probe.png` (pre), `post-reboot-probe.png` (post)

---

## Classification

| Tag | Item |
|-----|------|
| proximate | DRM/NVT panel unblank `R107_NATIVE_UNBLANK_FAILED` |
| not cause | 平行视窗 FWUI remount / fantasy magic-QQ / parallel-restore |
| not cause this incident | SF T2 vendor bake |
| recovery | reboot; no product rollback |

If blackscreen returns **only** when opening QQ magic dual-pane, re-open QQ-parallel rollback (`landscape-parallel\qq-parallel-fix-20261106\rollback-qq-db.cmd`) as A/B — that would still be app-window stress, not proof FWUI remount broke panel.
