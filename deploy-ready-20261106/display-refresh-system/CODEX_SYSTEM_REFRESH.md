# 系统级显示刷新策略 — deploy-ready（非 App 胶水）
hardware_success_claimed=false
date: 2026-11-06 Asia/Hong_Kong
视角: ColorOS OplusScreenMode / 产品刷新配置工程

## 问题（系统）
- 面板 DisplayMode 含 144；`mSupportMaxRefreshRate=144`
- 产品配置 `/my_product/etc/refresh_rate_config.xml`：
  - `ratemagic="8750R60_90_120"`
  - `<config maxrefreshsettings="3" .../>` → 设置高刷档被截断到 120
  - **未声明** `extremeHighEnable` / `defaultMaxRate` / `support144Hz`
- 结果：`mDefaultMaxRate=120`，`mExtremeHighEnable=false`，`mExtremeHighRateItems: []`，用户/peak 设置无法落到 144
- Framework（`oplus-services` `OplusRefreshRateConfigs`）已具备 `SETTING_MODE_144` / `FPS_144HZ` / ExtremeHigh 路径；缺的是**产品配置接通**

## 明确否决
- 按包名改 `rateId`（抖音/汽水等）— 不可维护，已卸试验模块
- `SUPPORT_144HZ_FOR_SPECIAL_PACKAGE` 白名单路线 — 同属胶水

## 本包改动（仅全局 config 一行）
原:
`maxrefreshsettings="3"`
改:
`maxrefreshsettings="4" defaultMaxRate="144" extremeHighEnable="true" support144Hz="true"`
**未修改**任何 `<item package=...>` 行；**未改** ratemagic（避免在未对照完整 rate 表前拆映射）。

## 验证门禁（ABA）
1. 装 `tb371fc_system_refresh_policy-trial.zip` → 重启
2. 检查 `dumpsys oplusscreenmode`：`isExtremeHighEnable` / `mDefaultMaxRate` / `mCurrentPickRate` / ExtremeHighRateItems
3. 设置里是否出现/可选 144；`settings get system peak_refresh_rate`
4. 多第三方热打断 + gfxinfo（微信/抖音/汽水）对比装前基线
5. 失败：`touch remove` 卸模块重启；成功：把同 diff 合入 ROM my_product，去掉 Magisk

## 汽水 path B
独立项：libsysoptimizer applyNative 崩溃缓解，**不是**跟手方案；长期应收口到 ART/runtime 策略。

## 文件
- `refresh_rate_config.xml`（系统策略稿）
- `tb371fc_system_refresh_policy-trial.zip`
- 证据基线见 `../follow-finger-20261106/` 与 `SYSTEM-REFRESH-STRATEGY-20261106.md`

## 系统策略 ABA 结果 2026-11-06 13:48 Asia/Hong_Kong
已装 `tb371fc_system_refresh_policy`（仅改全局 config，无包名行）：

**已生效（产品配置接通）**
- mMaxRefreshSettings=4（原 3）
- mDefaultMaxRate=144.0（原 120）
- mExtremeHighEnable=true（原 false）
- mCurrentPickMode=4
- Display 用户峰值投票 physical max=144

**仍未落到实帧**
- mCurrentPickRate / SF render 仍 120
- isExtremeHighSettingOn=false；mExtremeHighRateItems 仍 []
- WINDOW_REQUEST 锁 120；PreferredRefreshRateId=[2,2,2,3]（无 144 档映射）
- brightnessBlock 路径仍把优选打到 rateId 3

**系统层下一刀（非 App）**
- 查清 `ratemagic` / PreferredRefreshRate 默认表如何生成 mode→rateId（应对 144 需含第 5 档）
- 对照真·OPD2413/同面板产品的 rate 表与 magic；必要时改产品 rate 表而非包名
- 禁止走 SUPPORT_144HZ_FOR_SPECIAL_PACKAGE

hardware_success_claimed=false
