# DURATION-BOUNDS-20261106 — live vs donor SF duration safe-bound probe

**时间:** 2026-11-06 Asia/Hong_Kong（约 17:40）  
**hardware_success_claimed=false**  
**范围:** 只读。禁止 Magisk duration / 禁止 flash / 禁止 vendor bake apply。

## 结论（一句话）

**SAFE bake subset = NO。仍 BLOCKED。**  
Donor 与 live 的 `surfaceflinger` **字节级相同**；donor `vendor/build.prop` 的 duration 段是唯一「随发行镜像出厂」的宽松上界，但树内 **没有** donor 实机 144Hz `dumpsys`；Magisk 紧预算 6944444/8500000 **已本机 BOOT HANG**；仅开 `use_phase_offsets_as_durations=1` 而不清掉 / 改写 live `high_fps_*` **不安全**。

## 1. 活机只读快照（本轮）

| 项 | 值 | 来源 |
|----|-----|------|
| BuildId | `OPD2413_16.0.10.600(CN01)` | `getprop ro.build.display.id` |
| device | TB371FC | live |
| `/system/bin/surfaceflinger` SHA256 | `e5dbb77ee6500e41d2ce752f719eda235b18d8b8f130d14096a17d8087b44850` | `su sha256sum` = probe 文件 |
| activeMode | **144.00 Hz**（周期 ≈ 6944444 ns / 6.94 ms） | dumpsys |
| mWorkDuration / mReadyDuration | **8.89 / 10.94** ms | dumpsys |
| app / SF duration | **8888888 / 10944444** ns | dumpsys PhaseOffsets |
| app / SF phase | **1000000 / -4000000** ns | dumpsys（与 live `high_fps_*` 一致） |
| `debug.sf.use_phase_offsets_as_durations` | 空 | getprop |
| `debug.sf.late/early*.duration` | 全空 | getprop |
| `debug.sf.enable_advanced_sf_phase_offset` | 1 | getprop |
| `debug.sf.high_fps_late_app_phase_offset_ns` | 1000000 | getprop + vendor |
| `debug.sf.high_fps_late_sf / early / early_gl *_phase_offset_ns` | -4000000 | getprop + vendor |
| refresh XML MD5 | `35db38f8c85758c372546c707513642c` | `/my_product/etc/refresh_rate_config.xml` |

证据落盘：
- `deploy-ready-20261106/sf-duration-vendor-bake/live-dumpsys-duration-20261106-173937.txt`
- `deploy-ready-20261106/sf-duration-vendor-bake/live-getprop-sf-20261106-173937.txt`
- `follow-finger-20261106/sf-vendor-bake-probe/surfaceflinger.bin`

## 2. Donor 对照（文件，非第二台实机）

| 项 | Donor | 证据文件 |
|----|-------|----------|
| 镜像/树 | `original/OPD2413_16.0.10.600_CN01.zip` → `donor-tree/` / `donor-tree-case/` | 目录存在 |
| `system/.../bin/surfaceflinger` SHA256 | **`e5dbb77e…` 与活机完全相同**（`fc /b` 无差异） | 本轮哈希 |
| BuildId 关系 | 同系 OPD2413_16.0.10.600；活机显示 `(CN01)` | getprop vs zip 名 |
| `vendor/build.prop` duration 段 | 见下表「Donor 列」 | `donor_vendor_build.prop.sf-lines.txt` / `donor-tree-case/vendor/build.prop` |
| `high_fps_*_phase_offset_ns` | **整段不存在** | `Select-String high_fps` 无命中 |
| donor 144Hz dumpsys | **树内不存在** | 全树搜 `donor*dump*` / `mWorkDuration.*donor` 无实机 dumpsys |
| `advanced_sf_offsets.xml` | `SfDurationPercentage`；144 有 140–157，部分 `AppDuration=10333333` | `advanced_sf_offsets_donor.xml` |
| 本机 XML 消费 | 未证明（SF/composer 无路径串；QtiSFExtension 空） | `BLOCKED.md` 既有结论 |

### SF 二进制字符串（live ≡ donor）

两端均含：
- `debug.sf.use_phase_offsets_as_durations`
- `debug.sf.late/early/earlyGl .app/.sf .duration`
- `debug.sf.high_fps_*_phase_offset_ns`
- `sfDurationMapToFps:` / `qtiUpdateWorkDurations`

**未**在二进制中找到字面量 `8888888` / `10944444` / `13666666` / `10500000` / `6944444`。  
找到周期常量：`8333333`（120Hz）、`16666666`（60Hz），以及 `1000000` / `4000000`（与 live phase 默认一致量级）。  
→ 活机 8888888/10944444 是 **props 空时运行时映射/默认**（偏 120 预算），不是 donor duration 字面量，也不是编译进 bin 的 144 紧预算。

## 3. Bounds 总表（live vs donor vs Magisk hang）

| key / 度量 | Live（开机正常 @144） | Donor vendor（发行镜像 props） | Magisk trial（本机 BOOT HANG） |
|------------|----------------------|--------------------------------|--------------------------------|
| `use_phase_offsets_as_durations` | 空 | **1** | **1** |
| `late.app.duration` | 空 | **13666666** | **6944444** |
| `early.app.duration` | 空 | **13666666** | **6944444** |
| `earlyGl.app.duration` | 空 | **13666666** | **6944444** |
| `late.sf.duration` | 空 | **10500000** | **8500000** |
| `early.sf.duration` | 空 | **10500000** | **8500000** |
| `earlyGl.sf.duration` | 空 | **10500000** | **8500000** |
| `high_fps_late_app_phase_offset_ns` | **1000000** | *absent* | **6944444**（被改写） |
| `high_fps_late_sf_phase_offset_ns` | **-4000000** | *absent* | **8500000** |
| `high_fps_early_phase_offset_ns` | **-4000000** | *absent* | **6944444** |
| `high_fps_early_gl_phase_offset_ns` | **-4000000** | *absent* | **8500000** |
| dumpsys app/SF duration | 8888888 / 10944444 | **未知**（无 dumpsys） | 未取得（卡开机） |
| mWorkDuration @144 | 8.89 ms | **未知** | n/a |
| 相对 144 周期 6944444 | work **>** 1 帧（8.89） | props **≈2 帧**（13.67）/ SF 10.5 | props **=1 帧** 紧预算 |

### 数值边界解读（仅基于真实文件，非猜测「应设多少」）

| 边界 | ns（app / sf） | 状态 |
|------|----------------|------|
| **已证不安全（下紧）** | 6944444 / 8500000 + flag=1 + high_fps 同步改写 | 本机 Magisk BOOT HANG — `SF-DURATION-BOOT-HANG-NOT-ADOPTED.md` / `TRIAL.md` |
| **活机默认（开机 OK）** | 有效 duration 显示 8888888 / 10944444；duration props 空 + high_fps phase | 当前跟手未对齐 144 周期 |
| **Donor 出厂 props（镜像可启动）** | 13666666 / 10500000 + flag=1；**无** high_fps | 在 OPD2413 发行 `vendor/build.prop`；**未**在 TB371FC 验证；**无** 144 dumpsys |
| **XML AppDuration=10333333** | 仅 donor `advanced_sf_offsets` version 4–6 | 本机未证明消费该 XML → **不能**当 bake 安全值 |

## 4. SAFE bake subset？

| 候选 | 是否 SAFE（可起草 apply 包） | 证据 |
|------|------------------------------|------|
| 仅 `use_phase_offsets_as_durations=1`，不动 duration / 保留 live `high_fps_*` | **NO** | 既有根因：会把 ±phase（-4000000/1000000）当 duration；见 `FLUENCY-SF-ROOTCAUSE.md` |
| Magisk/草案紧预算 6944444/8500000 | **NO** | 本机 BOOT HANG |
| Donor 原样 duration 段 13666666/10500000 + flag=1，且 **删掉** live high_fps（拓扑对齐 donor） | **未证 SAFE on TB371FC** | Donor 镜像含此 props → 证明「某 OPD2413 vendor 如此出厂可启动」，但：① 无 donor@144 dumpsys；② 数值比当前 8.89 **更松**，不能当作「对齐 144 跟手」的目标界；③ 从未在本机 boot 测过 |
| Donor duration + 保留 live high_fps 的杂交 | **NO** | 任一侧发行树均未出现此组合 |

→ **不存在**「已证明在 booting donor @144、且不含 hung Magisk 组合」的最小 SAFE 子集可拿来 deploy-ready。  
**本轮不起草 bake 文件、不 apply。**

## 5. 树内「曾成功 144 duration」检索

只引用真实命中：
- `deploy-ready-20261106/sf-duration-144-trial/TRIAL.md` + `RESULT-BOOT-HANG-NOT-ADOPTED.md` → **失败**
- `VENDOR-BAKE-DRAFT.md` 已标 **SUPERSEDED**（数值即 hang 配方）
- **无** md/txt 记录「本机或同系机 144 duration props 开机成功 + dumpsys 改善」

## 6. 栈健康（本轮复核）

| 项 | 状态 |
|----|------|
| 刷新 XML | live `35db38f8…` |
| Pen V4 super | 文档基线 `7b1c6736…`（本轮未刷、未改） |
| Luna Magisk path B | 模块 **无** `disable`（启用） |
| `tb371fc_sf_duration_144` / dynframe / vrr / refresh Magisk | 均有 **`disable` 空文件** |

## 7. 唯一下一步（仍只读/离线，不碰 Qin 实机 bake）

1. **取得 donor 拓扑的 boot 证明：** 在可回滚 VM/备机上，用 **donor 原样** props（flag=1 + 13666666/10500000，**删除** high_fps_*）做 vendor 启动，抓 144Hz `dumpsys` 的 mWorkDuration。  
2. 若该组合能开机：再单独评估是否值得跟手（预期 work 可能 ≥13ms，未必优于现状）。  
3. **在此之前：** 保持 BLOCKED；禁止 Magisk duration；禁止把 6944444 配方写回任何 bake 草案当 deploy-ready。

## 相关路径

- 本文件：`deploy-ready-20261106/sf-duration-vendor-bake/DURATION-BOUNDS-20261106.md`
- `.../BLOCKED.md`（同步更新）
- `follow-finger-20261106/FLUENCY-SF-NEXT.md`
- `follow-finger-20261106/SF-DURATION-BOOT-HANG-NOT-ADOPTED.md`
- `donor-tree-case/vendor/build.prop`（donor duration 段）
- `follow-finger-20261106/sf-vendor-bake-probe/surfaceflinger.bin`

## UPDATE 2026-11-06 ~17:59 — donor LOOSE Magisk 实机证伪

| 候选 | 结果 |
|------|------|
| Magisk donor LOOSE 13666666/10500000 + flag=1 + high_fps=同档宽松 | **本机 BOOT HANG**（已回滚） |
| Magisk 紧预算 6944444/8500000 | **本机 BOOT HANG**（既有） |

→ Magisk 路径对 duration 全关闭。Vendor bake 仍未在 TB371FC 证明；需 VM/备机。

