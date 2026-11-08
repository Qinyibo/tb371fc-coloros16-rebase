# VENDOR-BAKE-DRAFT — SF duration 144（仅离线，禁止 Magisk 再试）

**hardware_success_claimed=false**  
**实机 Magisk 同配方已 BOOT HANG（见 RESULT-BOOT-HANG-NOT-ADOPTED.md）**

## 目标（刷写前必须 VM/备机验 boot）
在 endor/build.prop 落地 duration 模式，且 high_fps_* 为 **正 duration（ns）**，对齐 144 周期 6944444。

## 建议草案（未刷、未验证）
`
debug.sf.enable_advanced_sf_phase_offset=1
debug.sf.use_phase_offsets_as_durations=1
debug.sf.late.app.duration=6944444
debug.sf.late.sf.duration=8500000
debug.sf.early.app.duration=6944444
debug.sf.early.sf.duration=8500000
debug.sf.earlyGl.app.duration=6944444
debug.sf.earlyGl.sf.duration=8500000
debug.sf.high_fps_late_app_phase_offset_ns=6944444
debug.sf.high_fps_late_sf_phase_offset_ns=8500000
debug.sf.high_fps_early_phase_offset_ns=6944444
debug.sf.high_fps_early_gl_phase_offset_ns=8500000
`

对照 donor 原值（60 路径偏大，且实机 vendor 当前缺失整段）：
`
late.app=13666666 / late.sf=10500000 / use_phase_offsets_as_durations=1
`

## 门禁
1. 先完成 my_product refresh ROM bake（EXEC-FOR-CODEX.md）——独立、已 Magisk 证明。
2. vendor 改动另开刷写候选 + 回滚 donor-images/vendor.img。
3. 禁止 Magisk system.prop/resetprop 再试本机。

---

## SUPERSEDED 2026-11-06 17:20
本草案数值（6944444/8500000）即 Magisk BOOT HANG 配方，**不得**再当 deploy-ready。  
现状见：`deploy-ready-20261106/sf-duration-vendor-bake/BLOCKED.md`。
