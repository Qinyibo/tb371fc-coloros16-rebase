$ErrorActionPreference = "Continue"
$ringDir = "D:\TB371FC-release\clean-rebase-20261104\blackscreen-ring"
New-Item -ItemType Directory -Force -Path $ringDir | Out-Null
$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$log = Join-Path $ringDir ("ring-" + $ts + ".log")
Set-Content -LiteralPath (Join-Path $ringDir "CURRENT.txt") -Value ("CURRENT`r`n" + $log) -Encoding ascii
Write-Output ("START_RING " + $log)
# Prefer root buffers when available; fall back to non-root
$adb = "adb"
& $adb logcat -c 2>$null | Out-Null
# Start detached continuous capture
$arg = "-NoProfile -ExecutionPolicy Bypass -Command `"& { adb logcat -v threadtime *:V 2>&1 | Out-File -FilePath '" + $log + "' -Encoding utf8 -Append }`""
Start-Process -FilePath "powershell.exe" -ArgumentList $arg -WindowStyle Hidden
Start-Sleep -Seconds 2
if (Test-Path -LiteralPath $log) {
  $len = (Get-Item -LiteralPath $log).Length
  Write-Output ("RING_ALIVE bytes=" + $len + " path=" + $log)
} else {
  Write-Output "RING_MISSING_FILE"
}
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and $_.CommandLine -like "*logcat*" } | Select-Object ProcessId,Name,CommandLine | Format-List
