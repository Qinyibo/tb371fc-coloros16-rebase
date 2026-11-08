# 黑屏/无法唤醒 抓证（自然复现后立刻跑；插 USB 自醒要注明）
$out = "D:\TB371FC-release\clean-rebase-20261104\blackscreen-$(Get-Date -Format yyyyMMdd-HHmmss)"
New-Item -ItemType Directory -Force -Path $out | Out-Null
"note: mark if USB plug woke device" | Out-File "$out\NOTE.txt"
adb logcat -d > "$out\logcat-all.txt"
adb shell dmesg > "$out\dmesg.txt"
adb shell dumpsys power > "$out\dumpsys-power.txt"
adb shell dumpsys display > "$out\dumpsys-display.txt"
adb shell "su -c 'ls -la /sys/fs/pstore; cp -a /sys/fs/pstore /data/local/tmp/pstore-copy 2>/dev/null; ls -la /data/local/tmp/pstore-copy'" | Out-File "$out\pstore-ls.txt"
adb pull /data/local/tmp/pstore-copy "$out\pstore" 2>$null
adb shell "su -c 'logcat -b all -d'" > "$out\logcat-all-root.txt"
Write-Output "DONE $out"
