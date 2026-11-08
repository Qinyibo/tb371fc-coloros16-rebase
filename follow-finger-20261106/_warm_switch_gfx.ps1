$ErrorActionPreference = "Continue"
$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$base = "D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106"
$out = Join-Path $base ("warm-switch-gfx-" + $ts)
New-Item -ItemType Directory -Force -Path $out | Out-Null
Set-Content -LiteralPath (Join-Path $out "OUTPATH.txt") -Value $out -Encoding ascii
Write-Output ("OUT=" + $out)

function Get-PidMap {
  $map = @{}
  foreach ($pkg in @("com.tencent.mm","com.ss.android.ugc.aweme","com.luna.music")) {
    $pid = (adb shell "pidof $pkg").Trim()
    $map[$pkg] = $pid
    Write-Output ("PID $pkg=$pid")
  }
  $map | Out-String | Set-Content -LiteralPath (Join-Path $out "pids-before.txt") -Encoding utf8
  return $map
}

function Reset-Gfx($pkg) {
  adb shell "dumpsys gfxinfo $pkg reset" | Out-Null
}

function Dump-Gfx($pkg, $tag) {
  $path = Join-Path $out ("gfx-$tag-$pkg.txt")
  adb shell "dumpsys gfxinfo $pkg" | Out-File -FilePath $path -Encoding utf8
  Select-String -LiteralPath $path -Pattern "Total frames|Janky frames|High input|50th percentile|90th percentile|95th percentile|99th percentile|Missed Vsync|deadline missed" | ForEach-Object { $_.Line } | Out-File -FilePath (Join-Path $out ("gfxsum-$tag-$pkg.txt")) -Encoding utf8
}

function Dump-Sm($pkg, $tag) {
  adb shell dumpsys oplusscreenmode | Out-File -FilePath (Join-Path $out ("sm-$tag-$pkg.txt")) -Encoding utf8
  Select-String -LiteralPath (Join-Path $out ("sm-$tag-$pkg.txt")) -Pattern "mCurrentPickRate|PreferredRefresh|control panel|AppSwitchBoost|mAppSwitchBoostType|current mode|mActiveRenderFrameRate|mActiveSfDisplayMode|PRIORITY_WINDOW" | Select-Object -First 30 | ForEach-Object { $_.Line } | Out-File -FilePath (Join-Path $out ("smsum-$tag-$pkg.txt")) -Encoding utf8
}

function Warm-Start($pkg, $activity) {
  adb shell "am start -W -n $pkg/$activity" | Out-File -FilePath (Join-Path $out ("am-$pkg.txt")) -Append -Encoding utf8
  Start-Sleep -Seconds 2
}

$pids0 = Get-PidMap
# Ensure apps are already running - if missing, start once then treat subsequent as warm
if (-not $pids0["com.tencent.mm"]) { adb shell "monkey -p com.tencent.mm -c android.intent.category.LAUNCHER 1"; Start-Sleep 4 }
if (-not $pids0["com.ss.android.ugc.aweme"]) { adb shell "monkey -p com.ss.android.ugc.aweme -c android.intent.category.LAUNCHER 1"; Start-Sleep 4 }
if (-not $pids0["com.luna.music"]) { adb shell "monkey -p com.luna.music -c android.intent.category.LAUNCHER 1"; Start-Sleep 4 }
$pids1 = Get-PidMap
$pids1 | Out-String | Set-Content -LiteralPath (Join-Path $out "pids-warm.txt") -Encoding utf8

# Reset gfx counters
foreach ($pkg in @("com.tencent.mm","com.ss.android.ugc.aweme","com.luna.music")) { Reset-Gfx $pkg }

# Warm interrupt cycle: Douyin -> WeChat -> Luna -> Douyin -> WeChat (NO force-stop)
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
  Write-Output ("CYCLE $i -> $($c.pkg)")
  Warm-Start $c.pkg $c.act
  Dump-Sm $c.pkg ("c$i")
  # brief interaction wait for frames
  Start-Sleep -Seconds 3
}

# After warm switches, dump gfx
Dump-Gfx "com.tencent.mm" "after"
Dump-Gfx "com.ss.android.ugc.aweme" "after"
Dump-Gfx "com.luna.music" "after"

$pids2 = Get-PidMap
$pids2 | Out-String | Set-Content -LiteralPath (Join-Path $out "pids-after.txt") -Encoding utf8

# SF active mode snippet
adb shell dumpsys SurfaceFlinger 2>$null | Select-String -Pattern "refresh|Refresh|vsync|active mode|Display 0|144|120" | Select-Object -First 40 | ForEach-Object { $_.Line } | Out-File -FilePath (Join-Path $out "sf-grep.txt") -Encoding utf8

Write-Output "DONE warm-switch"
Get-ChildItem $out | Format-Table Name,Length
Get-Content (Join-Path $out "gfxsum-after-*.txt") -ErrorAction SilentlyContinue
Get-ChildItem $out -Filter "gfxsum-*" | ForEach-Object { Write-Output ("==== " + $_.Name + " ===="); Get-Content $_.FullName }
