# VRR TouchIdle OFF — A-on 自测（config PASS，跟手未过门）

**时间:** 2026-11-06 15:03 Asia/Hong_Kong  
**hardware_success_claimed=false**

## Config 验收
| 项 | 值 |
|----|----|
| VRR MD5 | `495ad3fc5ae9b4abbced79df54eb64db` |
| TouchIdleBean | mEnable=false hw=false sw=false |
| mSwWhiteMap | `{}` |
| PickRate / Preferred | 144 / [4,4,2,4] |
| dynframe | DISABLED `910955b1…` |

## gfx（reboot 后 monkey 开三应用 + am start×8 + adb swipe；非主观真指）
目录：`vrr-touchidle-A-on-20261106-150310/`  
同 PID：mm=9285 aweme=11175 luna=9202

| App | frames | janky% | High input | p90 |
|-----|--------|--------|------------|-----|
| WeChat | 624 | 15.22 | 320 | 20ms |
| Douyin | 510 | 30.39 | 676 | 36ms |
| Luna | 992 | 33.47 | 1291 | 46ms |

**不可据此宣称跟手成功。** 需登录态真指暖打断 + B-off 对照。

## 下一步 Codex
1. 用户登录三应用后真指滑动暖切 ABA  
2. B：`touch .../tb371fc_vrr_touchidle_off/disable` + reboot 对照  
3. 并行：真指 `getevent -lt /dev/input/event4` 量 NVT 间隔 vs 6.94ms  
4. 次级：SF mWorkDuration=8.89 vs 144 周期
