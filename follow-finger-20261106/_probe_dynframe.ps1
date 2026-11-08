$ErrorActionPreference = "Continue"
$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$out = "D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\dynframe-probe-" + $ts
New-Item -ItemType Directory -Force -Path $out | Out-Null
Write-Output ("OUT=" + $out)

# Pull live configs
adb shell "su -c 'cat /my_product/etc/sys_dynamic_frame_config.xml'" | Out-File (Join-Path $out "sys_dynamic_frame_config.live.xml") -Encoding utf8
adb shell "su -c 'md5sum /my_product/etc/sys_dynamic_frame_config.xml /my_product/etc/oplus_vrr_config.json'" | Out-File (Join-Path $out "md5.txt") -Encoding utf8
adb shell "su -c 'cat /my_product/etc/oplus_vrr_config.json'" | Out-File (Join-Path $out "oplus_vrr_config.live.json") -Encoding utf8

# AppSwitchBoost related strings from jar on device (strings via toybox)
adb shell "su -c 'toybox strings /system/framework/oplus-services.jar'" | Out-File (Join-Path $out "oplus-services-strings.txt") -Encoding utf8
Select-String -LiteralPath (Join-Path $out "oplus-services-strings.txt") -Pattern "AppSwitchBoost|appSwitchBoost|BoostType|DynamicFrame|targetFramerate|High input|mAppSwitch" | Select-Object -First 80 | ForEach-Object { $_.Line } | Out-File (Join-Path $out "appswitch-strings.txt") -Encoding utf8

# Display / SF mode
adb shell dumpsys display | Out-File (Join-Path $out "display.txt") -Encoding utf8
Select-String -LiteralPath (Join-Path $out "display.txt") -Pattern "mMode=|fps=|144|120|peakRefresh|renderFrameRate|Active mode|DisplayMode" | Select-Object -First 50 | ForEach-Object { $_.Line } | Out-File (Join-Path $out "display-grep.txt") -Encoding utf8

# Count targetFramerate values in live dynframe
$live = Get-Content (Join-Path $out "sys_dynamic_frame_config.live.xml") -Raw
Write-Output ("targetFramerate120 count=" + ([regex]::Matches($live, 'targetFramerate="120"')).Count)
Write-Output ("targetFramerate144 count=" + ([regex]::Matches($live, 'targetFramerate="144"')).Count)
Write-Output ("--- appswitch strings ---")
Get-Content (Join-Path $out "appswitch-strings.txt") -ErrorAction SilentlyContinue
Write-Output "--- display grep ---"
Get-Content (Join-Path $out "display-grep.txt") -ErrorAction SilentlyContinue
Write-Output "--- md5 ---"
Get-Content (Join-Path $out "md5.txt")
