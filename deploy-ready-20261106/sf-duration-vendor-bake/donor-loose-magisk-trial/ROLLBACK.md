# ROLLBACK — SF donor-loose Magisk trial

**时间:** 2026-11-06 Asia/Hong_Kong  
**hardware_success_claimed=false**  
**模块 id:** `tb371fc_sf_duration_donor_loose`  
**旧挂机模块** `tb371fc_sf_duration_144`（6944444/8500000）保持 **disable**，不要启用。

## 本 trial 写入的 props（唯一）
```
debug.sf.use_phase_offsets_as_durations=1
debug.sf.late/early/earlyGl.app.duration=13666666
debug.sf.late/early/earlyGl.sf.duration=10500000
debug.sf.high_fps_late_app / early_phase = 13666666
debug.sf.high_fps_late_sf / early_gl = 10500000
```
说明：high_fps 写成 **同档 donor 宽松值**，避免 flag=1 时把 live 的 -4000000/1000000 当 duration；**不是**挂机紧值 6944444/8500000。

## 回滚（首选，adb 仍能进）
```
adb shell su -c "touch /data/adb/modules/tb371fc_sf_duration_donor_loose/disable"
adb reboot
```
验证：`getprop sys.boot_completed` → 1；`getprop debug.sf.late.app.duration` → 空；dumpsys mWorkDuration 回到 ~8.89。

## 回滚（开机卡住但 adb device 可见 — 上次挂机同路径）
```
adb wait-for-device
adb shell su -c "touch /data/adb/modules/tb371fc_sf_duration_donor_loose/disable"
adb reboot
```

## 回滚（adb 全无）
1. 进 bootloader：`adb reboot bootloader` 或按键  
2. `fastboot devices`（Qin: `C:\android-sdk\platform-tools\fastboot.exe`）  
3. 若 Magisk 可从 recovery 删模块目录；或刷回未改 vendor（本 trial **未**改 vendor 分区镜像）  
4. vendor 备份：`sf-duration-vendor-bake/vendor_build_live_pre_loose_trial.prop`（MD5 fe6f8d95…）— 仅文件备份，分区未 flash。

## 禁止
- 启用 `tb371fc_sf_duration_144`（紧值挂机配方）
- ART/GC/OEM/freq/白名单叠加
- 同时启用 dynframe / vrr Magisk