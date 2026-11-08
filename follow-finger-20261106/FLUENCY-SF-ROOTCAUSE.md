# SF mWorkDuration 根因（只读结论 + 已选下一跳）

**时间:** 2026-11-06 Asia/Hong_Kong  
**hardware_success_claimed=false**

## 实机证据（2026-11-06 15:17）
- activeMode vsyncRate=**144.00 Hz**（周期 ≈ **6.94 ms**）
- mWorkDuration=8.89 / mReadyDuration=10.94
- PhaseOffsets：app duration=8888888 ns；SF duration=10944444 ns；app phase=1000000；SF phase=-4000000
- 与 144 周期错配：work 预算仍停在 ~120Hz 量级（8.89ms）

## Prop 实况（live）
| key | live |
|-----|------|
| debug.sf.use_phase_offsets_as_durations | 空 |
| debug.sf.late/early *.duration | 全空 |
| debug.sf.enable_advanced_sf_phase_offset | 1 |
| debug.sf.high_fps_late_app_phase_offset_ns | 1000000 |
| debug.sf.high_fps_late_sf_phase_offset_ns | -4000000 |
| ro.surface_flinger.set_touch_timer_ms | 2000 |
| ro.surface_flinger.game_default_frame_rate_override | 60 |

## Donor OPD2413（donor-tree-case/vendor/build.prop）
Donor 写有（实机 vendor 无）：
```
debug.sf.use_phase_offsets_as_durations=1
debug.sf.late.app.duration=13666666
debug.sf.early.app.duration=13666666
debug.sf.earlyGl.app.duration=13666666
debug.sf.early.sf.duration=10500000
debug.sf.earlyGl.sf.duration=10500000
debug.sf.late.sf.duration=10500000
```
donor game_default_frame_rate_override=120；live/system=60（非本 trial）。

## 根因判定
1. 主因：SF 在 144 面板下仍用非 144 对齐的 work/ready duration（8.89/10.94），触控打断后合成相位偏晚。
2. 配置层缺口：实机未落地 donor 的 use_phase_offsets_as_durations+*.duration。
3. 危险：只开 use_phase_offsets_as_durations=1 不改写 high_fps_*，会把 -4000000/1000000 当成 duration。必须成组写入。

## 已选下一跳
可逆 Magisk `tb371fc_sf_duration_144`：成组 duration 模式 + 144 周期预算（app=6944444, sf=8500000）。  
路径：deploy-ready-20261106/sf-duration-144-trial/ + TRIAL.md。同协议 ABA；不赢则 disable。

## 非杠杆
dynframe / VRR TouchIdle-off 已否定；禁止 jar bind / ART/GC/OEM/freq/白名单。

## 证据
- follow-finger-20261106/sf-live-20261106-1517.txt
- follow-finger-20261106/sf-live-filter-20261106-1517.txt
- follow-finger-20261106/sf-props-20261106-1517.txt
- follow-finger-20261106/sf-live-vs-donor-20261106.txt
- follow-finger-20261106/sf-prop-hunt-donor.txt

## 试验更新（2026-11-06 15:32）
Magisk 	b371fc_sf_duration_144 **开机卡住** → 已 disable 回滚成功。  
路径关闭：见 SF-DURATION-BOOT-HANG-NOT-ADOPTED.md。  
下一跳改走 my_product ROM bake 主线 + 离线 vendor duration 草案（sf-duration-144-trial/VENDOR-BAKE-DRAFT.md），禁止再 Magisk 试 duration。
