# 144 基线跟手 / High input latency — 下一步（sys6）

**时间：** 2026-11-06（Asia/Hong_Kong）  
**hardware_success_claimed=false**

## 当前度量（刷新策略已 ABA 通过）
| 项 | 值 |
|----|----|
| PickRate / SF / Render | **144**（live `oplusscreenmode` + `dumpsys display`） |
| PreferredRefreshRateId | `[4,4,2,4]`；control panel:4 |
| AppSwitchBoost | `true`；**Type=0**；MaxTemp=47 |
| ExtremeHighEnable | true（SettingOn=false） |
| NVT 触控 | `NVTCapacitiveTouchScreen`；`/proc` 有 `nvt_*`；sysfs `NVT-ts` |
| 解锁态 High input latency（同日早前暖切） | 微信 **155**；抖音 **593**；汽水 **1082** |
| dynframe 配置 | 实机 **89× `targetFramerate="120"`**，**0× 144** |
| dynframe 实机 MD5 | `910955b13710e2174b88f45506972467` |

## 主因候选（最窄系统层）
**`sys_dynamic_frame_config.xml` 仍按 120 给 DynamicFrameRate / OverScroller / 窗口动画定目标帧，与已切到 144 的 ScreenMode/SF vsync 错配。**

证据链：
1. ScreenMode 已投票 144，`mActiveSfDisplayMode`/`mActiveRenderFrameRate`=144  
2. jar 字符串显示 `OplusDynamicFrameRate*` / `targetFrameRate` / `AppSwitchBoost` 同栈  
3. 产品 dynframe 全表 `targetFramerate="120"`（含 type 10001/10003 列表滑动）  
4. 非触控节点缺失问题（NVT 在线）；非 PickRate 回落 120（第三方热启已 144）

次级杠杆（本轮不优先改）：`appSwitchBoostType`（当前 0，已 enable）；`oplus_vrr_config.json` 中抖音 sw_whitelist_3rd=[30]（adfr_enable=false）。

## 下一跳部署（已打包，可逆 Magisk）
路径：`D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\dynframe-144-trial\`
- `tb371fc_dynframe_144-trial.zip`
- `TRIAL.md`（含 MD5 / 回滚）
- 内容：仅 bind `my_product/etc/sys_dynamic_frame_config.xml`，全部 `120→144`

### Codex 一次执行
```text
adb push D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\dynframe-144-trial\tb371fc_dynframe_144-trial.zip /data/local/tmp/
adb shell su -c 'magisk --install-module /data/local/tmp/tb371fc_dynframe_144-trial.zip'
adb reboot
# 开机后：
adb shell su -c 'md5sum /my_product/etc/sys_dynamic_frame_config.xml'
# 验收：微信/抖音/汽水已登录且进程仍在；只用 am start 热切；禁止 force-stop/冷启脚本
# dumpsys gfxinfo <pkg> 看 High input latency；主观打断跟手
```

### 回滚
禁用/删除 Magisk 模块 `tb371fc_dynframe_144` → 重启 → dynframe MD5 回到 `910955b1…`

## 验收门禁（用户标准）
- 多第三方已打开（登录态）热/温打断切换  
- **禁止** 单应用反复测、force-kill 脚本冒充流畅  
- 长期层：产品 dynframe / ScreenMode；通过后 bake-in 进 `my_product`（与 refresh XML 同路径思路）

## 新 dump 目录
- `follow-finger-20261106\live-sys6-20261106-143713\`
- `follow-finger-20261106\live-sys6-root-20261106-143854\`
- `follow-finger-20261106\dynframe-probe-20261106-143918\`
- `follow-finger-20261106\warm-switch-gfx-*\`（屏灭时帧少；以解锁态 13:28 指标为基线）



## Exact trial hashes (rebuilt)
- stock: 910955b13710e2174b88f45506972467
- patched: fb92391a1a6a5c3486268a41aa95bc63
- zip: D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\dynframe-144-trial\tb371fc_dynframe_144-trial.zip


## Fresh warm metrics (2026-11-06 14:42 Asia/Hong_Kong)
Dir: `warm-switch-gfx-20261106-144225`
Same PIDs throughout (no cold): mm=9415 aweme=20485 luna=9376
| App | frames | janky% | High input latency | p90 |
|-----|--------|---------|--------------------|-----|
| WeChat | 430 | 16.74 | **669** | 23ms |
| Douyin | 311 | 29.26 | **379** | 46ms |
| Luna | 411 | 32.60 | **504** | 38ms |
PickRate remained 144 across cycles (smsum dumps).
