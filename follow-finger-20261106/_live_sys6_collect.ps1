$ErrorActionPreference = "Continue"
$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$out = Join-Path "D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106" ("live-sys6-" + $ts)
New-Item -ItemType Directory -Force -Path $out | Out-Null
Set-Content -LiteralPath (Join-Path $out "OUTPATH.txt") -Value $out -Encoding ascii
Write-Output ("OUT=" + $out)
adb shell dumpsys oplusscreenmode | Out-File -FilePath (Join-Path $out "oplusscreenmode.txt") -Encoding utf8
adb shell settings get system oplus_customize_screen_refresh_rate | Out-File -FilePath (Join-Path $out "settings-refresh.txt") -Encoding utf8
adb shell settings get system peak_refresh_rate | Add-Content -LiteralPath (Join-Path $out "settings-refresh.txt")
adb shell getprop persist.sys.oplus.anim_level | Add-Content -LiteralPath (Join-Path $out "settings-refresh.txt")
adb shell "ls /data/adb/modules" | Out-File -FilePath (Join-Path $out "magisk-modules.txt") -Encoding utf8
adb shell "cat /data/adb/modules/*/module.prop" | Add-Content -LiteralPath (Join-Path $out "magisk-modules.txt")
adb shell cat /proc/bus/input/devices | Out-File -FilePath (Join-Path $out "input-devices.txt") -Encoding utf8
adb shell "ls -l /sys/class/input/" | Out-File -FilePath (Join-Path $out "nvt-sysfs.txt") -Encoding utf8
adb shell "find /sys -maxdepth 6 -iname *nvt* 2>/dev/null" | Add-Content -LiteralPath (Join-Path $out "nvt-sysfs.txt")
adb shell dumpsys display | Out-File -FilePath (Join-Path $out "dumpsys-display.txt") -Encoding utf8
adb shell md5sum /my_product/etc/refresh_rate_config.xml | Out-File -FilePath (Join-Path $out "live-xml-md5.txt") -Encoding utf8
Write-Output "DONE"
Get-ChildItem $out | Format-Table Name,Length
$sm = Join-Path $out "oplusscreenmode.txt"
Select-String -LiteralPath $sm -Pattern "AppSwitchBoost|DefaultMaxRate|ExtremeHigh|PreferredRefresh|PickRate|control panel|mDefaultRateId|Version:|mAppSwitchBoostType|isAnimBoost|mVotes|PRIORITY" | Select-Object -First 60
