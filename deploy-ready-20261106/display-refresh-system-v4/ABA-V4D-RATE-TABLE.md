# 系统刷新策略 v4d — 产品表高档对齐 144（2026-11-06）

hardware_success_claimed=false

## 在 v4c 基础上
全表 `rateId="A-B-C-D"`：若 A 或 D 为 3（旧「高刷=120」），改为 4（144）。共 promote 1001 条。仍是**同一份** my_product `refresh_rate_config.xml`，不是按 App 另挂 Magisk。

例：抖音 `2-2-2-3`→`2-2-2-4`；微信包级 `3-2-2-3`→`4-2-2-4`；桌面 `3-2-2-3`→`4-2-2-4`。

## ABA
微信/抖音/汽水前台 `mCurrentPickRate=144`；面板 Preferred 仍 `[4,4,2,4]`；Version=20260107。

## 长期仍缺
1. ROM bake-in 该 XML（Magisk bind 试验态）
2. 主观热打断跟手验收 + High input latency 触控/合成深挖
3. 部分场景（拍摄/视频）故意锁 60/120 的条目需产品复核是否误升
