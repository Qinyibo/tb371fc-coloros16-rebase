# 鲸鲮 Office V2.1 系统预装 · STATUS 2026-11-06

`hardware_success_claimed=false`

Device: Qin `HA1W0JA3` (machineId `0bc7a3ae-6c23-4ea4-bc02-c2f0075b312d`)  
Work root: `D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\jingling-office-v21`  
Times: Asia/Hong_Kong

## 目标

刷入后默认存在「鲸鲮 Office 修改优化-内置字体版 V2.1」（包名 `com.yozo.office`）。

## 材料

| 项 | 值 |
| --- | --- |
| 源 APK | `C:\Users\Administrator\Downloads\鲸鲮Office修改优化-内置字体版V2.1.apk` |
| APK SHA-256 | `0CC7977DB6C35EAB3DD3E919800B06D59D0035A819F30FA464726AEB5E508461` |
| 大小 | 454404881 |
| package | `com.yozo.office` |
| versionName | `3.1.3813.1` |
| versionCode | `313813` |
| 说明 | 改名「V2.1 内置字体」优化包；versionName 仍为上游 3.1.3813.1 |

## 部署方式

`/system` 仅剩约 83M，无法 remount 烘焙 454MB APK。  
采用 **Magisk 模块 systemize**（与 pen/music 同标准）：

- 模块 id：`tb371fc_jingling_office_v21`
- 路径：`$MODDIR/system/app/YozoOffice/YozoOffice.apk` → 运行时 `/system/app/YozoOffice/YozoOffice.apk`
- zip：`tb371fc_jingling_office_v21.zip`（Python `zipfile` 正斜杠；APK STORED）
- zip SHA-256：`CC67A744000E2F03724A313AEFFEE4647A248DB8AAD5D1715D7865AE738A9C99`

## 脚本

| 脚本 | 作用 |
| --- | --- |
| `flash-jingling-office.cmd` | 一键：SHA 门禁 → push zip → `magisk --install-module` → 卸 /data 用户装 → **reboot** → verify |
| `check-verify.cmd` | 模块启用、APK SHA、`pm path`、冷启 |
| `rollback-jingling-office.cmd` | `touch remove` → reboot → 确认模块清除 |
| `build-zip.py` | 重建 zip（Windows 勿用资源管理器压缩） |

## 真机结果（2026-11-06 ~23:35 Asia/Hong_Kong）RESULT=PASS

- Magisk `--install-module` 成功；**故意 reboot**（Magisk system/app 挂载必需）
- `pm path` = `/system/app/YozoOffice/YozoOffice.apk`
- `flags=[ SYSTEM … ]`，versionName `3.1.3813.1` / versionCode `313813`
- 模块内 APK SHA = `0cc7977d…e508461`（与源一致）
- 冷启：`am start -W -n com.yozo.office/.MainAppActivity` → Status ok，LaunchState COLD，落到 `WelcomePrivacyActivity`，pid 存在
- 其它模块仍在：dynframe / luna / sf_duration×2 / system_refresh_policy / vrr_touchidle_off

## 不动清单

T2 / refresh bake / FWUI / fantasy / pen / luna / interconnect / ART / GC / OEM spoof — **均未改**。

## 为何重启

一键刷入第 5 步会 `adb reboot`。Magisk 把 APK 挂进 `/system/app` 必须重启后才对 PackageManager 可见为 SYSTEM 预装；不是崩溃、也不是黑屏修复。
