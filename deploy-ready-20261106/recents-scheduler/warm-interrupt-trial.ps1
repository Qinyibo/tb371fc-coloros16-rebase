# 热打断跟手试跑（禁止 force-stop）
# 用法: powershell -File warm-interrupt-trial.ps1
# 主指标: 你的主观跟手；辅: 是否仍被系统杀死变成冷启动
$apps = @(
  @{pkg='com.ss.android.ugc.aweme'; act='.splash.SplashActivity'},
  @{pkg='com.tencent.mm'; act='.ui.LauncherUI'},
  @{pkg='com.tencent.mobileqq'; act='.activity.SplashActivity'},
  @{pkg='com.luna.music'; act='com.luna.biz.main.main.MainActivity'}
)
$out = "D:\TB371FC-release\clean-rebase-20261104\warm-interrupt-$(Get-Date -Format yyyyMMdd-HHmmss)"
New-Item -ItemType Directory -Force -Path $out | Out-Null
adb shell "input keyevent KEYCODE_WAKEUP"
Start-Sleep 1
# open all once (warm pool)
foreach ($a in $apps) {
  adb shell "am start -W -n $($a.pkg)/$($a.act)" | Out-File "$out\warm-$($a.pkg).txt"
  Start-Sleep 4
}
# interrupt cycles: no force-stop
1..3 | ForEach-Object {
  $c = $_
  foreach ($a in $apps) {
    $t0 = Get-Date
    $r = adb shell "am start -W -n $($a.pkg)/$($a.act)"
    $r | Out-File "$out\cycle$c-$($a.pkg).txt"
    # swipe up a bit (follow-finger proxy); coords for 1840x2944 portrait-ish
    adb shell "input swipe 920 2200 920 900 250"
    Start-Sleep 2
    adb shell "input swipe 920 900 920 2200 250"
    Start-Sleep 2
    "cycle=$c pkg=$($a.pkg) wall=$t0" | Out-File "$out\cycle$c-$($a.pkg).meta.txt"
  }
}
adb shell "dumpsys activity processes" | Select-String -Pattern 'com.ss.android.ugc.aweme|com.tencent.mm|com.tencent.mobileqq|com.luna.music' | Out-File "$out\processes-after.txt"
Write-Output "DONE $out"
