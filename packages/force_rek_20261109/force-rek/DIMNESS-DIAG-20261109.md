# Dimness after Force REK — read-only diagnosis

Asia/Hong_Kong 2026-11-09 ~20:35 (unattended, no writes)

## Live facts (HA1W0JA3, r108-force-rek #45)
- settings: screen_brightness=8191 (UI normal max), mode=0 manual, night_display=null/off, low_power=0
- sys.oplus.multibrightness=8191, min=222
- sysfs panel0-backlight: brightness=1023, max_brightness=2047, actual_brightness=0 (stub; not real BL), bl_power=0
- dumpsys: mCachedBrightnessInfo brightness/adjusted=8191, brightnessMax=8191, hbmMode=0, hbmTransitionPoint=Infinity, mHbmMode=off
- Range: normalMaximum=8191, RangeMaximum=10239 (HBM band unused)
- BrightnessEvent log: nits=0.0 always; mNits=null / mNitsToBacklightSpline=null
- mBrightnessCapForWearBedtimeMode=0.07480315 is Wear bedtime modifier static field — NOT active cap
- Earlier “mBrightness=0.0” was stale/misread; current Display Brightness=8191.0, screen ON

## Mapping math
- At UI max 8191 → backlight PWM 1023/2047 ≈ 50% of hardware scale
- Upper half (1024–2047) aligns with unused HBM range (8192–10239)
- Identity brightness↔backlight spline; no photometric nits curve

## Pre-Force-REK baseline
- boot-diag has no saved pre-REK backlight= vs settings= pair to compare
- Force REK path only panel REK 0xA0→0xA1 on resume; no evidence it rewrites brightness tables

## Hypothesis (ranked)
1. **Primary (architecture / HBM off):** Normal max maps to ~half PWM; HBM disabled (hbmMode=0, transition Infinity). Feels slightly dim at “max” even with picture OK. Not a black-screen / REK failure.
2. **Secondary:** Missing nits calibration (nits=0) → framework can’t do calibrated boost; raw mapping only.
3. **Unlikely Force REK causal:** REK success + R107=0 + visible UI; dimness ≠ panel not resumed.
4. **Ruled out as active cause:** Night Light, reading mode props null, low_power=0, Wear bedtime cap (not applied), actual_brightness=0 (broken node).

## Raise user brightness vs kernel bug?
- **User slider already at normal max (8191)** — raising settings further won’t help within normal range.
- **Not safe/useful in unattended mode** to poke sysfs >1023 (HBM territory) or change settings.
- Treat as **framework/HBM mapping / missing nits**, not Force REK blackscreen bug. hardware_success_claimed stays false for other reasons; this dimness alone shouldn’t block REK path claim of “panel woke”.
