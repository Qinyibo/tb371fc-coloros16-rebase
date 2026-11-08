# RESULT — donor-loose Magisk BOOT HANG（已回滚）

**时间:** 2026-11-06 Asia/Hong_Kong（约 17:54–17:59）  
**hardware_success_claimed=false**

## Applied
**YES** — Magisk `tb371fc_sf_duration_donor_loose` v1

## Props applied (confirmed via getprop during hang window)
- `use_phase_offsets_as_durations=1`
- `late.app.duration=13666666`（及其他 early/earlyGl app=13666666）
- `late/early/earlyGl.sf.duration=10500000`
- `high_fps_*` 同步写成同档宽松 13666666/10500000（**不是** hang 紧值 6944444/8500000）

## Boot
**FAIL** — adb `device` 可见，但 `sys.boot_completed` 在 ≥4 分钟内始终为空（与紧值 Magisk 同模式）。Props 已生效，SystemServer 未完成。

## Rollback
**OK** — `touch .../tb371fc_sf_duration_donor_loose/disable` + `adb reboot`  
恢复后：
- `boot_completed=1`，`wm size=1840x2944`
- duration props 空；`high_fps_late_app=1000000`
- `mWorkDuration=8.89` / `mReadyDuration=10.94` @144
- refresh XML MD5 `35db38f8…` 仍在
- 模块 disable：sf_duration_144、sf_duration_donor_loose、dynframe、vrr、refresh

## mWorkDuration after trial
未取得（卡开机）。回滚后仍 **8.89 ms**。

## Conclusion
**Magisk/runtime 注入 SF duration（紧值与 donor 宽松值）在本机 ColorOS16 均不安全。**  
跟手 duration 对齐只能走 **离线 vendor 镜像 bake**，且必须先在 VM/备机证明可开机；**禁止**再 Magisk-set 这组 props。

## Paths
- 本文件 / 模块 / ROLLBACK：`D:/TB371FC-release/clean-rebase-20261104/deploy-ready-20261106/sf-duration-vendor-bake/donor-loose-magisk-trial`
- 边界文档：`D:/TB371FC-release/clean-rebase-20261104/deploy-ready-20261106/sf-duration-vendor-bake/DURATION-BOUNDS-20261106.md`