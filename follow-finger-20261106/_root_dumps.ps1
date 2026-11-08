$ErrorActionPreference = "Continue"
$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$out = "D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\live-sys6-root-" + $ts
New-Item -ItemType Directory -Force -Path $out | Out-Null
Set-Content -LiteralPath (Join-Path $out "OUTPATH.txt") -Value $out -Encoding ascii
Write-Output ("OUT=" + $out)

adb shell "su -c 'ls /data/adb/modules'" | Out-File (Join-Path $out "magisk-ls.txt") -Encoding utf8
adb shell "su -c 'cat /data/adb/modules/*/module.prop'" | Out-File (Join-Path $out "magisk-props.txt") -Encoding utf8
adb shell "su -c 'cat /proc/bus/input/devices'" | Out-File (Join-Path $out "input-devices.txt") -Encoding utf8
adb shell "su -c 'getevent -p'" | Out-File (Join-Path $out "getevent-p.txt") -Encoding utf8
adb shell "su -c 'find /sys -maxdepth 7 -iname *nvt*'" | Out-File (Join-Path $out "nvt-sysfs.txt") -Encoding utf8
adb shell "su -c 'ls -l /proc/android_touch /proc/touchpanel 2>/dev/null; ls /proc | grep -i nvt'" | Out-File (Join-Path $out "touch-proc.txt") -Encoding utf8
adb shell "su -c 'ls /sys/class/drm; cat /sys/class/drm/card0-DSI-1/modes 2>/dev/null'" | Out-File (Join-Path $out "drm-modes.txt") -Encoding utf8
adb shell "su -c 'md5sum /my_product/etc/refresh_rate_config.xml; ls -l /my_product/etc/refresh_rate_config.xml; mount | grep my_product'" | Out-File (Join-Path $out "live-xml.txt") -Encoding utf8
adb shell "su -c 'head -c 2000 /my_product/etc/refresh_rate_config.xml'" | Out-File (Join-Path $out "xml-head.txt") -Encoding utf8
adb shell "su -c 'getprop'" | Out-File (Join-Path $out "getprop-all.txt") -Encoding utf8
adb shell "su -c 'ls -l /system_ext/framework/oplus-services.jar /system/framework/oplus-services.jar /my_product/etc/sys_dynamic_frame_config.xml /my_product/etc/oplus_vrr_config.json 2>/dev/null'" | Out-File (Join-Path $out "related-files.txt") -Encoding utf8
adb shell dumpsys oplusscreenmode | Out-File (Join-Path $out "oplusscreenmode.txt") -Encoding utf8

Write-Output "DONE"
Get-ChildItem $out | Format-Table Name,Length
Write-Output "--- magisk ---"
Get-Content (Join-Path $out "magisk-ls.txt")
Write-Output "--- live xml ---"
Get-Content (Join-Path $out "live-xml.txt")
Write-Output "--- xml head ---"
Get-Content (Join-Path $out "xml-head.txt")
Write-Output "--- nvt ---"
Get-Content (Join-Path $out "nvt-sysfs.txt") | Select-Object -First 40
Write-Output "--- touch proc ---"
Get-Content (Join-Path $out "touch-proc.txt")
Write-Output "--- related ---"
Get-Content (Join-Path $out "related-files.txt")
