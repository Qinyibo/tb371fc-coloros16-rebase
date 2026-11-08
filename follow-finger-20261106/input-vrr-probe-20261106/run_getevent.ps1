$ErrorActionPreference='Continue'
$base='D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\input-vrr-probe-20261106'
$geLog="$base\getevent-swipe-event4.raw.txt"
if (Test-Path $geLog) { Remove-Item $geLog -Force }

# start getevent in background via Start-Process redirected
$p = Start-Process -FilePath 'adb' -ArgumentList @('shell','getevent -lt /dev/input/event4') -RedirectStandardOutput $geLog -RedirectStandardError "$base\getevent-err.txt" -PassThru -NoNewWindow
Start-Sleep -Milliseconds 600
1..8 | ForEach-Object {
  & adb shell 'input swipe 920 2200 920 900 280' | Out-Null
  Start-Sleep -Milliseconds 300
}
Start-Sleep -Milliseconds 800
if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue }
# also kill remote getevent
& adb shell 'pkill -f "getevent -lt"' 2>$null | Out-Null
Start-Sleep -Milliseconds 300
Write-Output ("getevent_bytes=" + (Get-Item $geLog).Length)
Get-Content $geLog -TotalCount 30
