# SF donor-loose Magisk trial

**hardware_success_claimed=false**

## Why
紧值 Magisk 6944444/8500000 已 BOOT HANG。本轮只试 **donor 出厂宽松** 13666666/10500000 + flag=1。  
high_fps 同步写成同档宽松（非 hang 配方），避免负 phase 当 duration。

## Install
```
adb push D:/TB371FC-release/clean-rebase-20261104/deploy-ready-20261106/sf-duration-vendor-bake/donor-loose-magisk-trial/tb371fc_sf_duration_donor_loose-v1.zip /data/local/tmp/
adb shell su -c "magisk --install-module /data/local/tmp/tb371fc_sf_duration_donor_loose-v1.zip"
adb reboot
```

## Success criteria
- boot_completed=1
- getprop late.app.duration=13666666
- dumpsys mWorkDuration 相对 8.89 有变化（记录即可，不宣称跟手成功）

## Fail → ROLLBACK.md