# STATUS - QQ native FO + tablet login + stutter pass

**Device:** TB371FC ColorOS16 (Qin) HA1W0JA3
**Time:** 2026-11-06 ~21:50 Asia/Hong_Kong (UTC+8)
**hardware_success_claimed:** false
**Untouched KEEP:** SF T2 mWorkDuration=6.94 / mReadyDuration=8.50 / 144 Hz; appSwitchBoostType=2 (MD5 67a0e527); pen; luna path B; interconnect; Douyin FO intent preserved

## Classification legend (steering)

| Tag | Meaning |
|-----|---------|
| system/product policy | /my_product remount table / ScreenMode / rate tables |
| interim data patch | runtime fantasywindow.db (cloud may rewrite) |
| rejected glue | Magisk per-app / OEM-identity spoof / ART/GC/freq/whitelist / Magisk orientation glue |

## 1) QQ landscape (native FO, not magic)

**Package:** com.tencent.mobileqq 9.3.80 (HeyTap Market)

### Cause
Fantasy product + DB had fullorientation status=2 with large alwaysFullOrientActivities allowlist (not global FO). Magic was already status=2 + excludeDevice:FOLD|PAD - correctly left OFF (magic = fake landscape).

### Changes

| Change | Class | Status |
|--------|-------|--------|
| fantasywindow.db QQ FO -> status=1, body/config {"rao":"true","rotate_cam":"false"}; magic stays 2 | interim data patch | APPLIED (live) |
| /my_product/etc/fantasy/sys_full_orientation_managed.xml QQ+Douyin FO -> status=1 + same simple body via remount (MD5 stock 7aef2aef -> bake 5848af15) | system/product policy | APPLIED (durable seed) |
| Magisk FO/orientation module | rejected glue | not used |
| Magic-window enable for QQ | rejected (fake landscape) | not used |

### Live verify (LoginActivity focused)
- Task mode=fullscreen
- Config land, bounds Rect(0,0-2944,1840) / app 2944x1803
- mIsFullOrientation=true
- OplusFullOrientationAppConfig{mPackageName=com.tencent.mobileqq, mStatus=1, ...}
- Still requestedOrientation=PORTRAIT (app asks) - same pattern as Douyin native FO

### Scripts
- Interim DB: redeploy-qq-native.cmd / rollback-qq-native-db.cmd / probe/fw-native-qq-v1.db / probe/fantasywindow.before-qq-fo-20261106.db
- Product bake: product-fo-bake/apply-qq-fo-product.cmd / revert-qq-fo-product.cmd

## 2) QQ tablet-only login

### Cause (verified, not spoofed away)
- ro.build.characteristics=nosdcard,tablet
- ro.oplus.image.system_ext.device_type=tablet
- ro.oplus.vpp.device.type=pad / ro.vendor.config.lgsi.device.type=pad
- Runtime config sw796dp + xlrg (tablet form factor)
- Enabled RROs: android.overlay.oplus.tablet, com.oplus.android.launcher.overlay.tablet

### Live login UI (uiautomator)
Already shows password / one-tap / other / register - not a QR-only pad gate. Complaint maps to pad device channel / tablet session identity, not missing password UI.

### Attempted non-identity paths
| Path | Result |
|------|--------|
| Settings DB phone/pad toggle | none found |
| ColorOS pad-to-phone login setting | not found |
| displaycompat size for QQ | would letterbox vs FO fullscreen - not applied |
| Magisk/resetprop fake phone / characteristics | rejected glue - STOP per steering |

### Verdict
**BLOCKED without identity glue.** No safe system/product toggle found to make QQ treat device as phone. Do not stack OEM-identity Magisk props.

## 3) Remaining stutter (after type=2 KEEP)

### Preserved
- T2 6.94 / ready 8.50 / 144 Hz activeMode
- appSwitchBoostType=2 live
- No Magisk added this turn

### This pass (observational warm gfx; noisier than ABA B protocol)
| App | Janky | p50/p90 | High input latency |
|-----|-------|---------|--------------------|
| WeChat | 14.88% | 5 / 13 ms | 300 |
| Douyin | 45.41% | 15 / 57 ms | 204 |
| Luna | 34.91% | 12 / 85 ms | 216 |

Artifacts: follow-finger-20261106/fluency-stutter-pass-20261106-2147/

### Headroom / decisions
| Lever | Class | Verdict |
|-------|-------|---------|
| appSwitchBoostType=2 | system/product (already KEPT) | KEEP - do not revert on noisier sample |
| SF T2 6.94 | system/product | KEEP |
| Launcher hardcoded 120 vote | needs Launcher APK / Magisk | rejected glue / blocked (prior ABA A) |
| NVT / high input latency vs 144 | Input path; prior input-vrr-probe | no new product knob without Magisk/freq/whitelist - no change |
| Dynframe Magisk re-enable | rejected (prior ABA FAIL) | leave off |

**Stutter one-shot:** KEEP current stack; no revert; remaining subjective stutter dominated by High input latency + launcher 120 oscillation - neither fixable as clean product remount without APK/Magisk glue.

## Parallel FlexibleWindow UI
Still MATERIALS-BLOCKED (skipped).

## Not claimed
hardware_success_claimed=false. No subjective fluency win. No phone-mode login success claimed.