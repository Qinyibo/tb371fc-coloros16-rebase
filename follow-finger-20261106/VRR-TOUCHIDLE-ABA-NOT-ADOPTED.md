# VRR TouchIdle-off Magisk ABA — NOT ADOPTED (keep DISABLED)

**时间:** 2026-11-06 Asia/Hong_Kong  
**hardware_success_claimed=false**

## Bind ABA
| | A ON (trial) | B OFF (stock) |
|--|--------------|---------------|
| JSON MD5 | 495ad3fc5ae9b4abbced79df54eb64db | e21e0be326d37a0f431a91fef4d2dbc0 |
| TouchIdleBean | mEnable/hw/sw=false, mSwWhiteMap={} | mEnable/hw/sw=true, Douyin→[30] |
| PickRate | 144 | 144 |

## Warm proto8 (同 dynframe：8 轮 am start + adb swipe；同侧 SAME PID；禁 force-stop)
| App | A janky% | B janky% | A p90 | B p90 | A High/frames | B High/frames |
|-----|----------|----------|-------|-------|---------------|---------------|
| WeChat | 12.61 | **12.25** | 16ms | 17ms | 1.44 | 1.51 |
| Douyin | 32.21 | **19.80** | 32ms | **24ms** | 1.29 | 1.38 |
| Luna | 18.82 | **14.42** | 22ms | 24ms | 1.56 | **1.41** |

## Verdict
**不采纳 TouchIdle 全关。** 连续滑动负载下抖音/汽水 janky 在 stock（TouchIdle 开）明显更好。模块保持 `disable`。

### 机制注
TouchIdle 主要在「超时无触摸→降 TE/内容帧→再触摸爬升」。连续 adb swipe **几乎不进入 idle**，本 ABA 不能替代「停顿后再触摸」的主观验收；但连续负载下 OFF 也未显示收益，默认回滚。

## Dumps
- A: `vrr-A-on-proto8-20261106-150536/`
- B: `vrr-B-off-proto8-20261106-150755/`
- 早前 monkey A: `vrr-touchidle-A-on-20261106-150310/`

## Next (system-layer)
1. SF `mWorkDuration≈8.89ms` vs 144 周期 6.94ms（次级；勿 jar）
2. 真指停顿→再滑：`getevent -lt /dev/input/event4` + 主观（adb 注入不经 event4）
3. `TouchFrameChange` / `AppSwitchBoostType` — 需证据后再动
