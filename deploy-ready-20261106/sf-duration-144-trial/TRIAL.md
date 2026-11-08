# SF workDuration 144-aligned Magisk trial

**hardware_success_claimed=false**

## Hypothesis
Live SF reports mWorkDuration=8.89ms / mReadyDuration=10.94ms while activeMode=144Hz (period ~6.94ms).
Dump shows app duration=8888888 ns, SF duration=10944444 ns.
Live debug.sf.*.duration empty; use_phase_offsets_as_durations empty.
Donor OPD2413 vendor/build.prop ships use_phase_offsets_as_durations=1 + late/early durations — NOT present on running vendor.
Flipping only the bool without rewriting high_fps_*_phase_offset_ns would treat current -4000000/1000000 as durations (unsafe). This module sets duration mode + all duration values together for 144 period.

## Props (system.prop + post-fs-data resetprop)
```
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
debug.sf.enable_advanced_sf_phase_offset=1
```

## Install
```
adb push D:/TB371FC-release/clean-rebase-20261104/deploy-ready-20261106/sf-duration-144-trial/tb371fc_sf_duration_144-v1-trial.zip /data/local/tmp/
adb shell su -c "magisk --install-module /data/local/tmp/tb371fc_sf_duration_144-v1-trial.zip"
adb reboot
```

## Verify after reboot
```
getprop debug.sf.use_phase_offsets_as_durations
getprop debug.sf.late.app.duration
dumpsys SurfaceFlinger | grep duration
```

## ABA
Same warm protocol: follow-finger-20261106/_warm_switch_gfx.ps1 (WeChat/Douyin/Luna SAME PID, am start only).
If B not better: touch disable and reboot.

## Forbidden
- oplus-services.jar bind
- Re-enable dynframe / VRR TouchIdle-off
- ART/GC/OEM/freq/whitelist stack

## RESULT (2026-11-06)
**BOOT HANG — NOT ADOPTED.** Module disabled. See RESULT-BOOT-HANG-NOT-ADOPTED.md.
