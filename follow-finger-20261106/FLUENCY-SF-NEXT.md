# 跟手下一跳：SF workDuration vs 144（VRR/dynframe 均未采纳之后）

**时间:** 2026-11-06 Asia/Hong_Kong（17:40 边界探针）  
**hardware_success_claimed=false**

## 顶栏状态（2026-11-06 17:40）
- **刷新策略：已 live-bake** `/my_product/etc/refresh_rate_config.xml` MD5 `35db38f8…`；Magisk refresh **DISABLE**。
- dynframe / VRR TouchIdle-off / **sf_duration_144** 均 **DISABLE**（紧预算 Magisk = BOOT HANG）。
- Pen V4 super 基线 `7b1c6736…`；Luna Magisk path B **启用**。
- SF vendor bake：**仍 BLOCKED** — 见 `DURATION-BOUNDS-20261106.md`（SAFE subset = NO）。

## 边界探针结果（本轮只读）
| | Live @144 | Donor vendor props | Magisk hang |
|--|-----------|--------------------|-------------|
| SF bin SHA256 | `e5dbb77e…` | **相同** | — |
| flag `use_phase_offsets_as_durations` | 空 | 1 | 1 |
| app/sf duration props | 空 → dumpsys **8888888/10944444** | **13666666/10500000** | **6944444/8500000** |
| high_fps_* | 1000000 / -4000000 | **absent** | 被改写成 duration |
| mWorkDuration | **8.89** ms | **无 144 dumpsys** | n/a（卡开机） |

- 仅开 flag、保留 live high_fps → **不安全**（phase 会被当 duration）。
- Donor 出厂值 **未**在 TB371FC 验证；且比 8.89 更松，不能当「对齐 144」目标。
- **不起草 bake、不 apply。**

## 已关闭（Magisk 试验）
| 试验 | 结果 | 状态 |
|------|------|------|
| refresh_rate_config | PASS → live-bake | Magisk **DISABLE** |
| dynframe 120→144 | FAIL | **DISABLED** |
| VRR TouchIdle 全关 | NOT ADOPTED | **DISABLED** |
| SF duration 紧预算 | **BOOT HANG** | **DISABLED** |

## 当前实机（跟手相关）
- ScreenMode / SF activeMode **144 Hz**
- SF `mWorkDuration=8.89` / `mReadyDuration=10.94`（仍偏 120 预算）
- duration props 空；phase 来自 vendor `high_fps_*`
- NVT 在线；**真指**才走 `/dev/input/event4`

## 建议下一跳（工程师）
1. **VM/备机 only：** donor 拓扑 props（13666666/10500000 + flag=1，删除 high_fps）可回滚 boot → 抓 144 `dumpsys`（见 DURATION-BOUNDS §7）。
2. **主观跟手**（adb 无法替代）：微信/抖音/汽水登录态热打断。
3. **真笔：** Pen V4 已刷；无 CTN730 时 CoreService 无 PID = 预期——贴笔再验。
4. **勿再：** Magisk duration / dynframe / VRR；oplus-services.jar bind；ART/GC/OEM/freq/白名单；Qin 上 vendor bake apply。

## 证据
- `deploy-ready-20261106/sf-duration-vendor-bake/DURATION-BOUNDS-20261106.md`
- `deploy-ready-20261106/sf-duration-vendor-bake/BLOCKED.md`
- `follow-finger-20261106/FLUENCY-SF-ROOTCAUSE.md`
- `follow-finger-20261106/SF-DURATION-BOOT-HANG-NOT-ADOPTED.md`
- `follow-finger-20261106/sf-vendor-bake-probe/`
