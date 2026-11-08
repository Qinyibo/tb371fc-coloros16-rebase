# 144 基线跟手下一步：Input / VRR TouchIdle（dynframe FAIL 之后）

**时间:** 2026-11-06 Asia/Hong_Kong  
**hardware_success_claimed=false**

## 已关闭
- Refresh Magisk bake-in **PASS**（Preferred [4,4,2,4]，第三方 PickRate=144）
- dynframe 120→144 Magisk ABA **FAIL** → 模块 **DISABLED**（stock MD5 `910955b1…`）。**勿再启用 / 勿 bake**

## 本轮证据

### 1) NVT 触控 vs 144 vsync
| 项 | 值 |
|----|----|
| 节点 | `NVTCapacitiveTouchScreen` → `/dev/input/event4` |
| FW | `fw_ver=0x1A` PID=`0x6068` ABS 18400×29440 |
| sysfs | `/sys/bus/spi/drivers/NVT-ts`（无 report_rate 节点） |
| `/proc/nvt_*` | baseline/diff/raw/fw_version/fw_status 有；无 Hz |
| IRQ `NVT-ts` | 空闲计数 0（Edge gpio 68）；无产品 touch report-rate 表 |
| `adb input swipe` | **不经过** event4 → 无法用注入测硬件采样间隔 |
| 144 期望间隔 | ~6.94ms |

**结论：** 产品层无触控 Hz 可改表；硬件采样间隔需**真指滑动** `getevent -lt /dev/input/event4` 再算。当前不能据此做 Magisk。

### 2) InputDispatcher / Choreographer / SF
| 项 | 值 |
|----|----|
| dumpsys input | NVT 正常 TOUCH_MT；无显式 “paced to 120” 字段 |
| SF renderRate / activeMode | **144 Hz** |
| SF `mWorkDuration` | **8.89ms**（> 144 周期 6.94ms，偏 120 预算） |
| SF `mReadyDuration` | **10.94ms** |
| `presentationDeadlineNanos` @144 | 11944444 (~11.9ms) |
| `ro.surface_flinger.set_touch_timer_ms` | 2000 |
| `mIsDisableInputLowRateWindow` | **false** |
| `frameRateCategoryRate` | normal=60 high=**90**（hasArrSupport=false） |

SF 时长提示与 144 错配是**次级**候选（非 product JSON 一跳可改；勿动 jar）。

### 3) oplus_vrr_config.json — **主因候选**
实机 MD5 `e21e0be326d37a0f431a91fef4d2dbc0`  
`dumpsys oplus_vrr_service`：

- `TouchIdle switch: true hw: true sw: true adfr: true`
- Bean：`mEnable=true mHwEnable=true mSwEnable=true mAdfrEnable=false mTimeOut=3000 mLowestRate=50`
- `mSwWhiteMap`：抖音等 → **[30]**
- `OtiHighRefreshMode: false`
- `m144To120Enable: false`
- ScreenMode `PickRate=144` 同时 VRR TouchIdle 独立可降 TE/内容帧（与 PickRate 解耦）
- 微信/汽水不在 sw_whitelist，但仍吃 **HW TouchIdle**（timeout 后降，触摸再爬升 → High input latency）

与跟手症状对齐：多第三方暖打断 + 滑动启动瞬间 High input latency；dynframe 全表 144 未赢。

### 4) 既有 dump
- `input-vrr-probe-20261106/`（本轮）
- `fluency-after-144-baseline.txt` / `warm-switch-gfx-*` / `DYNFRAME-ABA-FAIL.md`
- perfetto-douyin-*（早前）

## 主候选
**关闭 product VRR TouchIdle（hw/sw），并清空 sw_whitelist_3rd** — 系统表，非 per-app rateId 胶水。

## 已打包 Magisk
`deploy-ready-20261106/vrr-touchidle-off-trial/`  
详见同目录 `TRIAL.md`（MD5/回滚）。

### Codex 一次执行（装机 + 暖打断）
```text
# 0) 确认 dynframe 仍 disable；refresh 仍启用
adb shell su -c 'ls /data/adb/modules/tb371fc_dynframe_144/; md5sum /my_product/etc/sys_dynamic_frame_config.xml'
# expect disable 文件存在；MD5 910955b13710e2174b88f45506972467

# 1) 安装
adb push D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\vrr-touchidle-off-trial\tb371fc_vrr_touchidle_off-trial.zip /data/local/tmp/
adb shell su -c 'magisk --install-module /data/local/tmp/tb371fc_vrr_touchidle_off-trial.zip'
adb reboot

# 2) 开机
adb wait-for-device
adb shell su -c 'md5sum /my_product/etc/oplus_vrr_config.json'
# expect 495ad3fc5ae9b4abbced79df54eb64db
adb shell 'dumpsys oplus_vrr_service' | findstr /i TouchIdle
adb shell 'dumpsys oplusscreenmode' | findstr PickRate

# 3) 手动打开并登录 微信/抖音/汽水；记录 pidof；禁止 force-stop
# 4) 8 轮：仅 am start 热切 + 真机滑动；dumpsys gfxinfo 清后采 High input latency
# 5) 主观跟手；勿用安静 gfx 冒充成功

# B 回滚对照
adb shell su -c 'touch /data/adb/modules/tb371fc_vrr_touchidle_off/disable'
adb reboot
# md5 -> e21e0be326d37a0f431a91fef4d2dbc0
```

### 真指 NVT 采样（并行测量，非本 trial 依赖）
```text
adb shell getevent -lt /dev/input/event4 > D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\input-vrr-probe-20261106\getevent-finger.txt
# 真机快速滑动 2s 后 Ctrl-C；用相邻 ABS_MT_POSITION 时间戳算间隔，对照 6.94ms
```

## 次级（本包不做）
1. SF workDuration 8.89→对齐 144（phase/duration，慎改）
2. NVT 固件/驱动 report rate（无 product 表）
3. AppSwitchBoostType（仍 0）
4. **dynframe — 禁止**

## 验收门禁
多第三方已登录热切；主观打断跟手；`hardware_success_claimed=false` 直至主观过关。

## 装机状态（2026-11-06 15:03 Asia/Hong_Kong）
- Magisk 	b371fc_vrr_touchidle_off **ENABLED**，bind MD5=495ad3fc…
- Bean：mEnable=false hw=false sw=false；PickRate=144；dynframe 仍 DISABLED
- zip MD5=$zipMd5
- A-on 暖切 gfx 目录见 rr-touchidle-A-on-*；**hardware_success_claimed=false**（缺主观真指 ABA）
