$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$prefix = "E:\youxikaifa\work\today-20261109\boot-diag\panel-force-rek-$stamp"
Write-Host "PREFIX=$prefix"
adb shell "su -c 'dmesg -c >/dev/null; echo cleared'"
adb shell input keyevent KEYCODE_SLEEP
Start-Sleep -Seconds 8
adb shell dumpsys power | Select-String -Pattern "mWakefulness|Display Power"
adb shell input keyevent KEYCODE_WAKEUP
Start-Sleep -Seconds 2
adb shell input keyevent 82
Start-Sleep -Seconds 6
adb shell "su -c 'dmesg'" | Out-File -FilePath "$prefix-dmesg.txt" -Encoding utf8
adb shell "su -c 'dmesg'" | Select-String -Pattern "R10x_FORCE_REK|R94_|R107_|R108_RESX|nvt_check_fw|buf\[1\]=" | Out-File -FilePath "$prefix-dmesg-panel.txt" -Encoding utf8
adb shell dumpsys display | Out-File -FilePath "$prefix-display.txt" -Encoding utf8
adb shell dumpsys power | Out-File -FilePath "$prefix-power.txt" -Encoding utf8
adb shell "su -c 'for f in /sys/class/backlight/*/brightness /sys/class/backlight/*/actual_brightness; do echo \$f=\$(cat \$f 2>/dev/null); done; ls /sys/class/backlight/'" | Out-File -FilePath "$prefix-backlight.txt" -Encoding utf8
adb shell "su -c 'getprop sys.boot_completed; cat /proc/version; dumpsys SurfaceFlinger 2>/dev/null | head -5'" | Out-File -FilePath "$prefix-meta.txt" -Encoding utf8
Write-Host "--- panel ---"
Get-Content "$prefix-dmesg-panel.txt"
Write-Host "--- backlight ---"
Get-Content "$prefix-backlight.txt"
Write-Host "--- power ---"
Select-String -Path "$prefix-power.txt" -Pattern "mWakefulness|Display Power" | Select-Object -First 12
Write-Host "SAVED_PREFIX=$prefix"
