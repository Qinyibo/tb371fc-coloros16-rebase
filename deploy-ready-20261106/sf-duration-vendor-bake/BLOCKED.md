# SF duration vendor/system bake — BLOCKED（不可部署）

**时间:** 2026-11-06 Asia/Hong_Kong（17:40 边界探针更新）  
**hardware_success_claimed=false**  
**禁止:** 再启用 Magisk `tb371fc_sf_duration_144` / 再 Magisk-set duration props（已 BOOT HANG）/ 禁止本机 vendor remount bake apply

## 结论
**不能产出 deploy-ready bake。SAFE bake subset = NO。**  
详见同目录 **`DURATION-BOUNDS-20261106.md`**（本轮只读边界探针完整表）。

已证明：
- 活机 `mWorkDuration` 由 SF 读取的 `debug.sf.*` 控制；Magisk 成组紧预算会开机卡住。
- 活机与 donor-tree `surfaceflinger` **SHA256 完全相同**（`e5dbb77e…`），默认 8888888/10944444 **不是** donor duration 字面量编译进 bin。
- Donor 发行 `vendor/build.prop` 有 flag=1 + 13666666/10500000 且 **无** high_fps；树内 **无** donor@144 dumpsys。
- 仅开 `use_phase_offsets_as_durations=1` 而保留 live high_fps（±4ms/1ms）→ **不安全**。

## 活机只读实况（2026-11-06 17:39 复核）
| 项 | 值 |
|----|-----|
| activeMode | 144.00 Hz（周期 ≈ 6.94 ms） |
| mWorkDuration / mReadyDuration | **8.89 / 10.94** ms |
| dumpsys app/SF duration | **8888888 / 10944444** ns |
| dumpsys app/SF phase | **1000000 / -4000000** ns（与 high_fps props 一致） |
| `debug.sf.use_phase_offsets_as_durations` | 空 |
| `debug.sf.*.duration` | 全空 |
| `debug.sf.enable_advanced_sf_phase_offset` | 1 |
| `debug.sf.high_fps_*_phase_offset_ns` | 1000000 / -4000000 / -4000000 / -4000000 |
| SF binary SHA256 | `e5dbb77ee6500e41d2ce752f719eda235b18d8b8f130d14096a17d8087b44850` |
| refresh XML MD5 | `35db38f8c85758c372546c707513642c`（已 live-bake） |
| `/vendor/build.prop` MD5 | `fe6f8d95b40efedfcdfc45cf05ba6ec7` |
| `/vendor/etc/display/advanced_sf_offsets.xml` MD5 | `14d75510091fe41c9a9d64d117723bb6` |

## 边界（摘自 DURATION-BOUNDS）
| 边界 | app/sf ns | 状态 |
|------|-----------|------|
| Magisk 紧预算 | 6944444 / 8500000 + high_fps 改写 | **本机 BOOT HANG** |
| 活机默认 | 有效 8888888 / 10944444（props 空 + phase） | 开机 OK，跟手未对齐 144 |
| Donor 出厂 props | 13666666 / 10500000 + flag=1，无 high_fps | 镜像可启动；**未**在 TB371FC / 无 144 dumpsys |
| XML AppDuration | 10333333（donor schema） | 本机未证明消费 |

## 单文件差异（donor vs live）— 仍不可直接 bake
### A. `/vendor/build.prop`
活机仅有 high_fps **phase** 段；donor 有 duration 段、**无** high_fps。  
本目录：`vendor_build_live.prop`、`donor_vendor_build.prop.sf-lines.txt`。

### B. `/vendor/etc/display/advanced_sf_offsets.xml`
schema 差巨大；本机 SF/composer **未证明消费**（QtiSFExtension 空）→ 换 XML 不能当已证修复。

## Magisk 路径（已关闭）
`deploy-ready-20261106/sf-duration-144-trial/` — BOOT HANG NOT ADOPTED。  
本轮确认 disable 文件仍在：`sf_duration` / `dynframe` / `vrr_touchidle` / `system_refresh_policy`。  
Luna path B 模块保持启用（无 disable）。

## 缺失证据（仍阻止 deploy-ready）
1. 任一组 duration props 在 **TB371FC ColorOS16** 上能开机的证明（donor 数值亦未在本机测）。
2. Donor（或同 SF 二进制设备）在 **144Hz** 下的 `dumpsys` mWorkDuration 实值。
3. （次要）XML 线：证明本机库打开 `advanced_sf_offsets.xml`。

## 唯一下一跳
按 `DURATION-BOUNDS-20261106.md` §7：在 **VM/备机** 用 donor 拓扑（flag=1 + 13666666/10500000，删除 high_fps）做可回滚 boot + 抓 144 dumpsys。  
**之前：** 不 vendor remount、不打 vendor 差分上 Qin、不重开 Magisk duration。

## 本目录文件
- `DURATION-BOUNDS-20261106.md`（本轮主交付）
- `BLOCKED.md`（本文件）
- `live-dumpsys-duration-20261106-173937.txt` / `live-getprop-sf-20261106-173937.txt`
- `advanced_sf_offsets_live.xml` / `advanced_sf_offsets_donor.xml`
- `vendor_build_live.prop` / `donor_vendor_build.prop.sf-lines.txt`
- 探针大文件：`follow-finger-20261106/sf-vendor-bake-probe/`

## 非杠杆（保持）
ART/GC/OEM/freq/白名单；dynframe / VRR TouchIdle-off / sf_duration Magisk 保持 disable。

## UPDATE 2026-11-06 ~17:59 Asia/Hong_Kong — donor-loose Magisk also HANG

实机 trial `tb371fc_sf_duration_donor_loose`（flag=1 + 13666666/10500000 + high_fps=同档宽松）**BOOT HANG**；已 disable 回滚，mWorkDuration 恢复 8.89。  
详见 `donor-loose-magisk-trial/RESULT-BOOT-HANG-ROLLED-BACK.md`。  
**结论升级：** 不仅紧值，**donor 宽松 Magisk 路径亦关闭**。下一跳仅离线 vendor.img 补丁 + VM/备机 boot 证明。


## UPDATE 2026-11-06 ~18:03 — offline vendor prep ready (NOT flashed)

`vendor-offline-prep/vendor_a-LIVE-sf-donor-loose.img` 已基于活机 dump 打好（build.prop MD5 fe6f8d95→cfb2330f）。  
**未 flash。** 详见 `vendor-offline-prep/README.md`。
