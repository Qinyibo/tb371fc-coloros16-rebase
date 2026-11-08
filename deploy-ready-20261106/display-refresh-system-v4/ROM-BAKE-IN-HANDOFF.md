# ROM bake-in handoff — refresh_rate_config.xml（Codex 一次执行）

**状态：材料就绪 / 本机未刷 ROM**  
`hardware_success_claimed=false`

## 已验证（Magisk ABA，2026-11-06）
- 实机与模块 MD5：`35db38f8c85758c372546c707513642c`
- `Version=20260107` 完整解析
- `mDefaultRateId=[4,4,2,4]`；`PreferredRefreshRateId=[4,4,2,4]`（systemui `NotificationShade_controlPanel`）
- `control panel:4`；微信/抖音/汽水 `mCurrentPickRate=144`
- **禁止** Magisk bind `oplus-services.jar`（已证实 bootloop）

## 交付物（Qin `D:`）
| 路径 | 用途 |
|------|------|
| `...\display-refresh-system-v4\bake-in\refresh_rate_config.xml` | 规范产品 XML（UTF-8 **无 BOM**） |
| `...\display-refresh-system-v4\bake-in\BAKE-IN.md` | 配方说明 |
| `...\display-refresh-system-v4\BAKE-IN-ABA-PASS.md` | ABA 证据 |
| `...\display-refresh-system-v4\RATE-TABLE-REVERSE.md` | rateId 反推 |
| `...\display-refresh-system-v4\product-config\magisk-module\` | 当前试验 Magisk（XML-only） |
| 本文件 `ROM-BAKE-IN-HANDOFF.md` | Codex 一步交接 |

## Codex 必须做的镜像步骤（本机未证明完整 my_product 重打包+刷写闭环，故停在 deploy-ready）
1. 取现行 `my_product` 镜像源（donor：`D:\TB371FC-release\clean-rebase-20261104\donor-images\my_product.img` 或当前刷机候选树）。
2. 解包 / 挂载后，**仅替换**：
   `my_product/etc/refresh_rate_config.xml`
   ← 复制 `bake-in\refresh_rate_config.xml`
3. 写入后校验：
   `MD5 == 35db38f8c85758c372546c707513642c`
   且文件为 UTF-8 **无 BOM**（首字节非 `EF BB BF`）。
4. 按既有 TB371FC ColorOS16 刷机流程重打包 `my_product`（或 super 内对应分区）并刷写；**不要**顺带塞入 `oplus-services.jar` 补丁。
5. 刷完后 **禁用/删除** Magisk 模块 `tb371fc_system_refresh_policy`，再跑 ABA：
   - `dumpsys oplusscreenmode` → Version `20260107`
   - `mDefaultRateId=[4,4,2,4]`；`PreferredRefreshRateId=[4,4,2,4]`；`control panel:4`
   - 热启微信/抖音/汽水 → `mCurrentPickRate=144`
6. `tb371fc_luna_heap_offset_fix` 保持独立，勿并入本 refresh 模块。

## 关键约束
- `defaultRateId` 必须是连字符元组 `4-4-2-4`（标量 `"4"` → `[4,0,0,0]` 失败）
- Preferred 来自 systemui item，不是裸 `<config>` 幻想属性
- 产品表高档位 A/D 组件 `3→4` 已进本 XML（1001 items）；勿再做 per-app Magisk rateId 胶水

## Flash 工具现状（Qin）
- 存在：`flash-candidate\tools\fastboot.exe`、`donor-images\my_product.img`
- **未**在本轮证明：从 bake-in XML → 重打包 my_product → 实机无 Magisk ABA 的完整闭环  
→ Codex 需用既有镜像构建脚本完成步骤 1–5；Grok 本轮停在 deploy-ready 材料。

## 更新
- 无歧义执行书：同目录 EXEC-FOR-CODEX.md
- 树补丁/打包：rom-stage/
