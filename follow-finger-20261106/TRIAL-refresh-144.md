# TRIAL ONLY — refresh 144 / ExtremeHigh 接线（未刷入）
hardware_success_claimed=false
date: 2026-11-06 Asia/Hong_Kong

## 现象
- 面板 DisplayMode 含 144Hz；OplusScreenMode `mSupportMaxRefreshRate=144` 但 `mDefaultMaxRate=120`、`mCurrentPickRate=120`。
- `mExtremeHighRateItems: []`；`extreme_high_enable=1` 不改变 isExtremeHighEnable。
- `/my_product/etc/refresh_rate_config.xml`：`ratemagic="8750R60_90_120"`，注释 rateId 仅到 120；`<config maxrefreshsettings="3" .../>` 无 ExtremeHigh 项。
- 抖音：`rateId="2-2-2-3" brightnessBlock="true"`。

## 假设
TB371FC ColorOS16 rebase 的 refresh 策略仍是 8750 手机 60/90/120 表，未接平板 144 档 → 跟手上限被策略封在 120。

## 建议验证（Codex / 源码）
1. 对比 donor OPD2413_16.0.10.600 同路径 `refresh_rate_config.xml` / ScreenMode Config 的 ratemagic、ExtremeHighRateItems、maxrefreshsettings。
2. 若 donor 有 144 / ExtremeHigh：做 **最小 overlay Magisk** 只替换该 xml（或等价 my_product 片段），ABA：同条件抖音 gfxinfo High input latency / janky + 主观跟手。
3. 禁止同时叠频率/白名单/schedtune。
4. 失败即回滚模块。

## 本地证据
D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\
