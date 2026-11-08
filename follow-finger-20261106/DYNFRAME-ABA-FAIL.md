# dynframe 144 Magisk ABA — FAIL (keep DISABLED)

**时间:** 2026-11-06 Asia/Hong_Kong  
**hardware_success_claimed=false**

## Bind ABA (config)
| | A ON | B OFF |
|--|------|-------|
| MD5 | fb92391a1a6a5c3486268a41aa95bc63 | 910955b13710e2174b88f45506972467 |
| targetFramerate 120/144 | 0 / 89 | 89 / 0 |
| PickRate / Preferred | 144 / [4,4,2,4] | 144 / [4,4,2,4] |

## Warm interrupt gfx (SAME PID within side; 8-cycle am start + swipe; no force-stop)
| App | A janky% | B janky% | A p90 | B p90 | A High/frames | B High/frames |
|-----|----------|----------|-------|-------|---------------|---------------|
| WeChat | 11.15 | 11.67 | 16ms | 16ms | 1.35 | 1.51 |
| Douyin | 23.79 | **20.93** | 25ms | 26ms | 1.37 | 1.36 |
| Luna | 20.04 | **15.45** | 26ms | **21ms** | 1.53 | **1.43** |

## Verdict
**不采纳 dynframe 全表 120→144。** 同协议下汽水/抖音 janky 与 High-input 比率未改善（汽水明显变差）。模块保持 `disable`；勿 bake-in。

## Dumps
- A: `follow-finger-20261106/dynframe-warm-20261106-144729/`
- B: `follow-finger-20261106/dynframe-B-off2-20261106-145143/`

## Next fluency candidates (narrow, system-layer)
1. Touch/Input path vs 144 vsync (NVT report rate / InputDispatcher / Choreographer) — primary after this FAIL
2. `oplus_vrr_config.json` 第三方 whitelist（adfr）— secondary
3. `AppSwitchBoostType`（当前 0 已 enable）— tertiary；需同条件改 type 对照，勿盲改

## Module state
`/data/adb/modules/tb371fc_dynframe_144/disable` present → stock dynframe live.
