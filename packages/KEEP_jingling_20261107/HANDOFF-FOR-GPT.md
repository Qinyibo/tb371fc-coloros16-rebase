# HANDOFF · GPT 刷机 · 2026-11-07

`hardware_success_claimed=false`

## 现状
- 设备序列号: `HA1W0JA3`
- 鲸鲮完整 ROM 刷入失败: super 写到 4/49，USB 超时(121)
- 退回 KEEP (pen-v4-on-e088) 也失败: super 第1块 USB 超时
- 设备多在 fastboot；换线/换口后再刷

## 用户要什么
1. 完整 ROM 一键刷入（不是 Magisk 小模块，不是只确认鲸鲮 APK）
2. 出问题可退回上一版 KEEP
3. 包里只要一个中文「一键刷入.cmd」

## 主包（鲸鲮已烤进 system）
`D:\TB371FC-release\ColorOS16_TB371FC_KEEP_jingling_20261107_CANDIDATE\`
- 双击: **一键刷入.cmd**（GBK；刷 super+boot+vbmeta；`wipe_userdata=false`）
- `images\super-KEEP-jingling.img` SHA256 `9845539c7c139cc08408bbc6f9a3d9c1653c0b84821e6170993f651df73c27cb`
- boot SHA256 `5b4acefcc109ece2d3b84ce646b3496de6dfe2dc4b33d459bd2557d4d9a38b3a`
- 鲸鲮: `/system/app/YozoOffice/YozoOffice.apk` SHA256 `0cc7977db6c35eab3dd3e919800b06d59d0035a819f30fa464726aeb5e508461`
- 脚本: `scripts\Invoke-R91-Clean.ps1 -Execute -Reboot`（已按 manifest 跳过 erase userdata）

## 退回 KEEP（无鲸鲮烤入）
`D:\TB371FC-release\clean-rebase-20261104\pen-sharing-compat\candidate-v4-on-e088\super-pen-v4-on-e088-OFFLINE.img`
- SHA256 `7b1c6736d45bf228a46df0e00dd2cd54e73cf1e36f6cf6a9bb08efbf2aba033d`
- boot: `D:\TB371FC-release\clean-rebase-20261104\magisk-update\boot-magisk-31100.img`（同上 `5b4acefc…`）
- vbmeta 可用主包 `images\vbmeta_a.img` / `vbmeta_system_a.img`

示例（设备须在 fastboot；建议 `-S 64M` 防超时）:

```
fastboot -s HA1W0JA3 -S 67108864 flash super <OFFLINE.img>
fastboot -s HA1W0JA3 flash boot_a <boot-magisk-31100.img>
fastboot -s HA1W0JA3 flash vbmeta_a <vbmeta_a.img>
fastboot -s HA1W0JA3 flash vbmeta_system_a <vbmeta_system_a.img>
fastboot -s HA1W0JA3 set_active a
fastboot -s HA1W0JA3 reboot
```

不要 erase userdata，除非用户明确要求清空。

## USB
整包容易超时。优先换线/直连主板口；分块用 `-S 64M` 或 `128M`。先前 `256M` 超时。

## 刷后核验

```
adb wait-for-device
adb shell getprop sys.boot_completed
adb shell pm path com.yozo.office
# 期望: package:/system/app/YozoOffice/YozoOffice.apk
```

## 不要做
- 不要把 Magisk zip `jingling-office-v21` 当成整包交付
- 不要默认走 delta 当「一键刷入」（用户要的是完整 ROM）
- 不要声称 hardware_success


## 11 月 7 日刷入流程修正

一键入口现复用 11 月 4 日成功的 bootloader fastboot 方式。完整主包 super 已预拆为 385 个不超过 32 MiB 的独立稀疏镜像，逐个调用 fastboot。离线按目标偏移重组的 SHA-256 与完整原镜像一致。只在某一块写入收到 OKAY 后更新断点，失败则停在该块。断点只适用于同一设备、同一镜像且期间未用其它工具写过 super 的情况；否则应从第 1 块开始。完整主包流程仍保留 wipe_userdata=false。

上一次 64 MiB 自动分块失败后，设备还能被枚举，但 getvar product 超时。本流程尚未上机执行，须先恢复 bootloader fastboot 响应。
