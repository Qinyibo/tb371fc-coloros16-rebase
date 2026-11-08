# 系统刷新策略 v4c — 长期试验通（2026-11-06）

hardware_success_claimed=false

## 实机 ABA（满解析 Version=20260107）
- Config: MaxRefreshSettings=4 DefaultMaxRate=144 ExtremeHighEnable=true
- mDefaultRateId=[4,4,2,4]
- mPanelRateData PreferredRefreshRateId=[4,4,2,4]
- control panel:4
- mCurrentPickMode=4 mCurrentDefaultRateId=4 mCurrentPickRate=144
- SF renderRate/activeMode=144（见 sf-v4c.txt）

## 生效配方（全局 <config> + ratemagic，零包名 rateId 行）
```
ratemagic="8750R60_90_120_144"
defaultRateId="4-4-2-4"   <!-- 必须是连字符四元组，不能写标量 4 -->
maxRefreshRateId="4"      <!-- 标量 -->
maxrefreshsettings="4" defaultMaxRate="144" extremeHighEnable="true" support144Hz="true"
```
UTF-8 **无 BOM**。Magisk 模块 `tb371fc_system_refresh_policy` bind `/my_product/etc/refresh_rate_config.xml`。

## 否决项
- 标量 `defaultRateId="4"` → Config 里变成 `[4,0,0,0]`，面板表不改，锁 120
- 仅 defaultMaxRate/maxrefreshsettings → PickMode=4 但 Preferred 仍 `[3,2,2,3]`
- Magisk 绑挂 patched `oplus-services.jar` → 卡开机动画，已 remove
- 按 App 打 rateId 胶水 — 用户否决

## 未完成（不算长期搞定）
1. ROM bake-in：把上述 XML 合入 my_product（Magisk 只是试验态）
2. AppSwitchBoost 打断是否仍投票 120
3. 多第三方热打断主观跟手 + High input latency（触控/合成）
