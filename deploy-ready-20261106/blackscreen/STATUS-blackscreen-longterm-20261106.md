# STATUS — Blackscreen cause & long-term fixability (2026-11-06 ~22:50 HKT)

**Device:** TB371FC ColorOS16 Qin HA1W0JA3  
**hardware_success_claimed:** false  
**KEEP:** T2 / 144 / type=2 / FWUI `19D32858…` / fantasy tables — **no rollback** (not implicated).

---

## User questions

1. 黑屏是怎么导致的？  
2. 能不能修复？  
3. 长期能修好吗？

---

## Mechanism (soft failure, not parallel)

| Layer | What happened |
|-------|----------------|
| Framework | `mWakefulness` could go Awake; `mScreenState=ON`; compositor still had a framebuffer (`blackscreen-probe.png` ~4.3 MB). Focus included NotificationShade / QQ Splash. |
| Brightness | Observed `mBrightness=0.0` while user saw black — backlight/panel path not lighting. |
| Kernel/panel | Repeated **`R107_NATIVE_UNBLANK_FAILED rc=-1`** and **`R94_NATIVE_COMPLETE_REK_FAILED -1 IRQ_CLOSED_DISPLAY_RETAINED`**, with `R104_PANEL_DEAD_POWER_ON` / `R94_PANEL_POST_ARMED` — **NVT/DRM panel unblank / reconnection failed**. |
| Userspace suspects today | FWUI remount, fantasy FO/magic, QQ pairs — **no DRM touch**; ring had **no** related FATAL. Recovery **without** rolling those back. |

**Soft vs hard:** **Soft** (software/firmware path stuck). `adb reboot` cleared R107 and restored light. Not a dead panel brick in this incident.

**Trigger context (not causation):** validating QQ 平行 around sleep/wake + power key can stress resume; does not prove fantasy config corrupted display.

---

## Can it be fixed? Long-term?

| Horizon | Answer |
|---------|--------|
| Immediate | **Yes for this incident** — reboot. Soft wake (`stayon` / KEYCODE_WAKEUP) was **not** enough once R107 stuck. |
| Product XML / fantasy / Magisk | **No** — wrong layer. |
| Long-term on this port | **Partially / uncertain.** Needs **kernel / panel (NVT) unblank & rail recovery** hardening on the TB371FC ColorOS16 port — compare working R94 panel driver / DT / DRM commits; add repro harness (rapid sleep/wake + ADB). **Not** claimable as `hardware_success` until a controlled soak shows zero R107 under the same stress. |
| If R107 returns **only** with QQ magic dual (v2 GuildBlank) | A/B with `rollback` of QQ relatedPage (already moved to v3). Still app-window stress hypothesis, not FWUI proof. |

### Deploy-ready next step (no hardware_success claim)

1. Keep artifact set under `blackscreen\` (dmesg R107, ring, probes).  
2. Optional soak script: N cycles `svc power stayon` / sleep / wake; count R107 — park under `blackscreen\soak\` when written.  
3. Kernel track: diff panel unblank / REK path vs known-good R94 tree on D: — **read-only inventory first**, no flash until user asks.

### Classification

| Tag | Item |
|-----|------|
| proximate | DRM/NVT `R107_NATIVE_UNBLANK_FAILED` |
| soft | reboot recovers |
| not cause | 平行视窗 FWUI / fantasy QQ / FO bulk / T2 |
| long-term | panel/kernel port work; product layer exhausted |

