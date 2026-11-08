# STATUS — 平行视界适配为何「没有」+ 本次修复 (2026-11-06 ~22:25 HKT)

**Device:** TB371FC ColorOS16 Qin HA1W0JA3  
**hardware_success_claimed:** false  
**KEEP:** SF T2, refresh 144, appSwitchBoostType=2, FO bulk for **non-magic** apps, no OEM spoof/Magisk identity

---

## 1) 用户为什么觉得「平行视界适配都没有」

不是产品表「没写 2888 条」，而是 **三层错位**：

| 层 | 之前状态 | 用户感知 |
|----|----------|----------|
| **A. 功能语义** | 上一轮 bulk 主要扩的是 **FullOrientation（原生全屏横屏）**，把微信等 FO 改成 `status=1 rao:true` | 看起来像「横屏有了」，但 **平行双窗没了**。公开文档写明：切 FO 全屏会丢掉双窗，不是最终目标 |
| **B. 运行库 vs 产品表** | Fantasy 产品 XML 里 magic≈2887 status=1，但多数 `installed=0`；机上已装第三方里 magic 行很少；QQ/抖音 magic=`status=2` + `excludeDevice:PAD` | 设置里看不到「适配名单」，抖音/QQ 被 PAD 排除 |
| **C. 设置壳** | `com.oplus.pscanvas` / FlexibleWindowUI **2.0.0** SHA=`01450E66…` 与 donor **相同**；SettingActivity 只有浮窗教程，没有旧包那种按应用平行列表 | 「平行视界」页死板、没有适配模块 |

根因一句话：**FO 全屏策略压过了 Magic Window；再加 PAD 排除 + 薄 UI，用户就看到「适配都没有」。**

Pre-bulk 对照：微信 FO 原本是 **`status=2`**（让平行优先）；bulk 改成 status=1 rao:true 后 dumpsys 出现 `mIsFullOrientation=true` / fullscreen land，双窗路径被冲掉。

---

## 2) 本次已修（产品 + 运行库，无伪装）

目录：`landscape-parallel\parallel-restore-20261106\`

| 改动 | 类 | 内容 |
|------|----|------|
| 机上有 magic 行的包（12） | product+DB | magic `status=1`，去掉 QQ/抖音 `excludeDevice:PAD` |
| 上述包的 FO | product+DB | 改回 **`status=2`**（平行优先）；微信 FO 按 public-source `rao:false` + 选择性 alwaysFullOrient |
| 微信 magic | DB(+rules) | `scaleWindow=-1`、`isDraggable`；另试 `defSwitch=magic`（v2 DB） |
| 其余无 magic 的 App | 不动 | 仍保留 bulk FO 横屏 |
| FlexibleWindowUI APK | **未换** | D:/Codex 日志搜不到异哈希材料 |

**Live product MD5:**  
- fantasy `e70effef1c1f579339eddb2baf34c058`  
- FO `2cc0d09033cad6e542864d21aaecb2cc`

**运行验证：**
- 抖音横屏：`mode=oplus-magic-windows` + TaskFragment（平行路径已通）
- 微信：配置已恢复平行优先；LauncherUI 单页时 Task 可能仍显示 fullscreen，打开会话后才出左右双窗（activityPairs: LauncherUI→*）。请用户横屏打开微信点进聊天确认双窗。
- QQ：magic 已 status=1；登录页可能仍全屏，进主界面后再看。

Apply: `parallel-restore-20261106\apply-parallel.cmd`（已执行；DB 现为 parallel-v2）

---

## 3) FlexibleWindowUI 旧材料搜索结论（NOT FOUND）

目标：SHA256 ≠ `01450E66939EAC2A0E188396244B1F59725E862342BE978CA60CD8E218BE7BB8`

**搜过的路径：**
- `D:\TB371FC-release\`（含 donor-tree / probe / R94 树 / public-source）
- `C:\Users\Administrator\.codex\`（sessions jsonl 全文命中多为现网 dumps，无异哈希 APK）
- `C:\Users\Administrator\agent-tools\`
- `D:\CodexBackups\`（RG35XX 备份，无 TB FlexibleWindowUI）
- `C:\Users\Administrator\.agents` / `.claude` / `.rpa_agent`
- 缺失：`D:\Codex`、`D:\codex`、`D:\.codex`、Cursor AppData 目录

**找到的 OplusFlexibleWindowUI.apk 仅 3 份，全部 = 现网哈希。**  
详见 `MATERIALS-SEARCH-20261106.txt`。

给用户粘贴给 Codex 的提取提示见同目录 `CODEX-PROMPT-extract-FlexibleWindowUI-zh.md`。

---

## 4) 用户如何验收

1. **横屏**打开 **抖音** → 应为平行/魔法窗口布局（非整屏 FO）。  
2. **横屏**打开 **微信** → 点进任意聊天，看是否左右双窗；可拖分割条。  
3. **QQ** 登录后横屏看是否进入平行。  
4. 设置 → 搜「平行视界」仍可能只有浮窗教程（UI 壳缺旧 APK，一次标死）。  
5. 其它 App 横屏：无 magic 规则的仍走 FO 全屏横屏（bulk 保留）。

回滚提示：`product-fo-bulk-20261106` 的 pre-bulk XML + `fantasywindow.pre-bulk.db`；或 `/data/local/tmp/sys_fo.pre-parallel-*.xml`。
## 5) Addendum �� prefs version align
Updated `fantasy_window_prefs.xml` stamps to product `20261107` (was 20260515/20260706/20260422) so factory bake is not treated as stale vs ROM-update channels.
DB redeployed parallel-v2 after prefs write.
Verify lines: AWEME/WECHAT task mode captured in verify/modes (see shell).

## 6) Runtime verify (HKT 2026-11-06 ~22:22)
| App | Task mode after landscape launch |
|-----|----------------------------------|
| ���� com.ss.android.ugc.aweme | **oplus-magic-windows** (confirmed) |
| QQ com.tencent.mobileqq | **oplus-magic-windows** (confirmed, may be bg) |
| ΢�� com.tencent.mm | Task still fullscreen at LauncherUI; FO=status2 magic=1 scaleWindow=-1 applied �� open a chat in landscape for dual-pane (activityPairs) |

UI shell FlexibleWindowUI still MATERIALS-BLOCKED (no alternate APK on disk).
T2 / 144 / type=2 / FO bulk for non-magic apps kept.
hardware_success_claimed=false
