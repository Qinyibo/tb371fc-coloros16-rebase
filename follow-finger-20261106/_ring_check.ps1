$ErrorActionPreference = "Continue"
Write-Output "=== blackscreen-ring listing ==="
Get-ChildItem -LiteralPath "D:\TB371FC-release\clean-rebase-20261104\blackscreen-ring" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 20 Name,Length,LastWriteTime | Format-Table -AutoSize
Get-ChildItem -LiteralPath "D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\blackscreen-ring" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 20 Name,Length,LastWriteTime | Format-Table -AutoSize
Get-ChildItem -LiteralPath "D:\TB371FC-release\clean-rebase-20261104\blackscreen-20261106-143538" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 20 Name,Length,LastWriteTime | Format-Table -AutoSize
Write-Output "=== capture script ==="
Get-Content -LiteralPath "D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\recents-scheduler\blackscreen-capture.ps1" -Raw
Write-Output "=== processes ==="
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and ($_.CommandLine -like "*blackscreen*" -or $_.CommandLine -like "*ring*") } | Select-Object ProcessId,Name,CommandLine | Format-List
Write-Output "=== recents-scheduler dir ==="
Get-ChildItem -LiteralPath "D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\recents-scheduler" -ErrorAction SilentlyContinue | Format-Table Name,Length,LastWriteTime -AutoSize
Get-ChildItem -LiteralPath "D:\TB371FC-release\clean-rebase-20261104\recents-scheduler" -ErrorAction SilentlyContinue | Format-Table Name,Length,LastWriteTime -AutoSize
