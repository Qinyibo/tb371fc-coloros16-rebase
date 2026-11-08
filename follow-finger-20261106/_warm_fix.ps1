$ErrorActionPreference = "Continue"
$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$out = "D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\warm-switch-gfx-" + $ts
New-Item -ItemType Directory -Force -Path $out | Out-Null
Write-Output ("OUT=" + $out)

# Wake + dismiss keyguard if possible
adb shell input keyevent 224
adb shell input keyevent 82
Start-Sleep -Seconds 1
adb shell dumpsys power | Select-String -Pattern "mWakefulness=|mHoldingDisplaySuspendBlocker|Display Power: state" | Out-File (Join-Path $out "power.txt") -Encoding utf8

function Get-AppPid($pkg) {
  $raw = adb shell ("pidof " + $pkg)
  if ($null -eq $raw) { return "" }
  return ([string]$raw).Trim()
}

$pkgs = @("com.tencent.mm","com.ss.android.ugc.aweme","com.luna.music")
$pidMap = @{}
foreach ($pkg in $pkgs) {
  $p = Get-AppPid $pkg
  if (-not $p) {
    adb shell ("monkey -p " + $pkg + " -c android.intent.category.LAUNCHER 1") | Out-Null
    Start-Sleep -Seconds 4
    $p = Get-AppPid $pkg
  }
  $pidMap[$pkg] = $p
  Write-Output ("PID " + $pkg + "=" + $p)
}
$pidMap.GetEnumerator() | ForEach-Object { $_.Key + "=" + $_.Value } | Set-Content (Join-Path $out "pids-warm.txt") -Encoding utf8

foreach ($pkg in $pkgs) { adb shell ("dumpsys gfxinfo " + $pkg + " reset") | Out-Null }

$cycles = @(
  @{pkg="com.ss.android.ugc.aweme"; act=".splash.SplashActivity"},
  @{pkg="com.tencent.mm"; act=".ui.LauncherUI"},
  @{pkg="com.luna.music"; act="com.luna.biz.main.main.MainActivity"},
  @{pkg="com.ss.android.ugc.aweme"; act=".splash.SplashActivity"},
  @{pkg="com.tencent.mm"; act=".ui.LauncherUI"},
  @{pkg="com.luna.music"; act="com.luna.biz.main.main.MainActivity"},
  @{pkg="com.ss.android.ugc.aweme"; act=".splash.SplashActivity"}
)
$i=0
foreach ($c in $cycles) {
  $i++
  Write-Output ("CYCLE " + $i + " -> " + $c.pkg)
  adb shell ("am start -W -n " + $c.pkg + "/" + $c.act) | Out-File (Join-Path $out ("am-c" + $i + ".txt")) -Encoding utf8
  Start-Sleep -Milliseconds 800
  # generate input frames: short swipes (no force-stop)
  adb shell input swipe 900 2000 900 900 180
  Start-Sleep -Milliseconds 400
  adb shell input swipe 900 900 900 2000 180
  Start-Sleep -Seconds 1
  adb shell dumpsys oplusscreenmode | Select-String -Pattern "mCurrentPickRate|control panel|AppSwitchBoost|current mode" | ForEach-Object { $_.Line } | Out-File (Join-Path $out ("smsum-c" + $i + ".txt")) -Encoding utf8
}

foreach ($pkg in $pkgs) {
  $safe = $pkg -replace '\.','_'
  adb shell ("dumpsys gfxinfo " + $pkg) | Out-File (Join-Path $out ("gfx-" + $safe + ".txt")) -Encoding utf8
  Select-String -LiteralPath (Join-Path $out ("gfx-" + $safe + ".txt")) -Pattern "Total frames|Janky frames|High input|50th percentile|90th percentile|95th percentile|99th percentile|Missed Vsync|deadline missed" | ForEach-Object { $_.Line } | Out-File (Join-Path $out ("gfxsum-" + $safe + ".txt")) -Encoding utf8
  Write-Output ("==== " + $pkg + " ====")
  Get-Content (Join-Path $out ("gfxsum-" + $safe + ".txt"))
}

foreach ($pkg in $pkgs) {
  $p2 = Get-AppPid $pkg
  Write-Output ("PID_AFTER " + $pkg + "=" + $p2 + " was=" + $pidMap[$pkg] + " same=" + ($p2 -eq $pidMap[$pkg]))
}
