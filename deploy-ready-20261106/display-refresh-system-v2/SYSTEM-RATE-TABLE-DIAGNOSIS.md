# TB371FC 系统刷新策略 v2 — 裁决（2026-11-06）

hardware_success_claimed=false

## 实机已通
Magisk 产品 config 增加 `defaultRateId="4" maxRefreshRateId="4"` 后：
- control panel:4；mPanelRateData=[4,4,2,4]
- PickRate/SF/微信/抖音/汽水 = 144
- 零包名 rateId 行

机制：即便 framework `getSettingModeIndex=min(mode,3)` 仍读 preferred 下标 3，表项已是 rateId 4→144。

## 离线报告修正
executor 建议的 oplus-services 一字节补丁（const/4 3→7）与「禁止 defaultRateId」**不要执行**：会与已验证的产品解冲突，且非必需。framework-patch 仅 ROM 长期备选。

## 固化
合入 my_product `refresh_rate_config.xml` 全局 config 上述属性。跟手剩余查触控/合成，禁止按 App 补丁。
