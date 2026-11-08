$ErrorActionPreference = "Continue"
$out = "D:\TB371FC-release\clean-rebase-20261104\warm-interrupt-$(Get-Date -Format yyyyMMdd-HHmmss)"
New-Item -ItemType Directory -Force -Path $out | Out-Null
$apps = @(
  @{pkg="com.ss.android.ugc.aweme"; cmp="com.ss.android.ugc.aweme/.splash.SplashActivity"},
  @{pkg="com.tencent.mm"; cmp="com.tencent.mm/.ui.LauncherUI"},
  @{pkg="com.tencent.mobileqq"; cmp="com.tencent.mobileqq/.activity.SplashActivity"},
  @{pkg="com.luna.music"; cmp="com.luna.music/com.luna.biz.main.main.MainActivity"}
)
function Get-PidMap {
  $m = @{}
  foreach ($a in $apps) {
    $p = (adb shell ("pidof " + $a.pkg)).Trim()
    if (-not $p) { $p = "NONE" }
    $m[$a.pkg] = $p
  }
  return $m
}
function Save-Env([string]$tag) {
  adb shell "su -c 'getprop init.svc.tb371fc-scheduler; cat /dev/tb371fc-schedtune/foreground/schedtune.boost; cat /dev/tb371fc-schedtune/foreground/schedtune.prefer_idle; getprop persist.sys.oplus.anim_level; cat /sys/class/kgsl/kgsl-3d0/min_pwrlevel'" | Out-File (Join-Path $out ("env-" + $tag + ".txt"))
  adb shell "cat /sys/class/thermal/thermal_zone0/temp; cat /sys/class/thermal/thermal_zone1/temp" | Out-File (Join-Path $out ("thermal-" + $tag + ".txt"))
}
adb shell input keyevent KEYCODE_WAKEUP
Start-Sleep 1
adb shell wm dismiss-keyguard
Save-Env "start"
foreach ($a in $apps) {
  adb shell ("am start -W -n " + $a.cmp) | Out-File (Join-Path $out ("warm-" + $a.pkg + ".txt"))
  Start-Sleep 5
  adb shell "input swipe 920 2100 920 900 280"
  Start-Sleep 2
}
$warmPids = Get-PidMap
$warmPids.GetEnumerator() | ForEach-Object { $_.Key + "=" + $_.Value } | Out-File (Join-Path $out "pids-after-warm.txt")
$summary = New-Object System.Collections.Generic.List[string]
$summary.Add("cycle,pkg,launchState,totalMs,pidBefore,pidAfter,pidChanged")
1..3 | ForEach-Object {
  $c = $_
  foreach ($a in $apps) {
    $before = (adb shell ("pidof " + $a.pkg)).Trim(); if (-not $before) { $before = "NONE" }
    $r = adb shell ("am start -W -n " + $a.cmp)
    $r | Out-File (Join-Path $out ("c" + $c + "-" + $a.pkg + ".txt"))
    $stateLine = ($r | Select-String "LaunchState:").Line
    $totalLine = ($r | Select-String "TotalTime:").Line
    $state = if ($stateLine) { ($stateLine -replace ".*LaunchState:\s*","").Trim() } else { "?" }
    $total = if ($totalLine) { ($totalLine -replace ".*TotalTime:\s*","").Trim() } else { "?" }
    Start-Sleep 1
    adb shell "input swipe 920 2200 920 800 220"
    Start-Sleep 1
    adb shell "input swipe 920 800 920 2200 220"
    Start-Sleep 2
    $after = (adb shell ("pidof " + $a.pkg)).Trim(); if (-not $after) { $after = "NONE" }
    $changed = if ($before -ne $after) { "YES" } else { "NO" }
    $summary.Add("$c,$($a.pkg),$state,$total,$before,$after,$changed")
  }
  Save-Env ("after-c" + $c)
}
$summary | Out-File (Join-Path $out "summary.csv")
$final = Get-PidMap
$cmp = New-Object System.Collections.Generic.List[string]
$cmp.Add("pkg,warmPid,finalPid,survived")
foreach ($a in $apps) {
  $w = $warmPids[$a.pkg]; $f = $final[$a.pkg]
  $surv = if (($w -ne "NONE") -and ($w -eq $f)) { "YES" } else { "NO" }
  $cmp.Add("$($a.pkg),$w,$f,$surv")
}
$cmp | Out-File (Join-Path $out "pid-survival.csv")
adb shell "su -c 'ls -lt /data/tombstones | head -6'" | Out-File (Join-Path $out "tombstones-end.txt")
Write-Output ("OUT=" + $out)
Get-Content (Join-Path $out "summary.csv")
Write-Output "--- survival ---"
Get-Content (Join-Path $out "pid-survival.csv")
Write-Output "--- tombstones ---"
Get-Content (Join-Path $out "tombstones-end.txt")
