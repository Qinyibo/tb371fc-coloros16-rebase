$ErrorActionPreference = "Continue"
$base = "D:\TB371FC-release\clean-rebase-20261104"
$xml = Join-Path $base "deploy-ready-20261106\display-refresh-system-v4\bake-in\refresh_rate_config.xml"
Write-Output "=== config attrs ==="
Select-String -LiteralPath $xml -Pattern "AppSwitch|appSwitch|appswitch|boostType|animBoost|defaultMaxRate|extremeHigh" | Select-Object -First 40
Write-Output "=== first config tag ==="
# read first 30 lines
Get-Content -LiteralPath $xml -TotalCount 30
Write-Output "=== donor my_product xml? ==="
$cands = @(
  "$base\donor-tree\my_product\etc\refresh_rate_config.xml",
  "$base\donor-tree\system\my_product\etc\refresh_rate_config.xml",
  "$base\donor-tree-case\my_product\etc\refresh_rate_config.xml",
  "$base\follow-finger-20261106\sys_dynamic_frame_config.xml",
  "$base\follow-finger-20261106\oplus_vrr_config.json"
)
foreach ($c in $cands) {
  Write-Output ("exists=" + (Test-Path -LiteralPath $c) + " " + $c)
  if (Test-Path -LiteralPath $c) {
    if ($c.EndsWith('.json')) { Get-Content -LiteralPath $c -TotalCount 40 }
    else { Get-Content -LiteralPath $c -TotalCount 15 }
  }
}
Write-Output "=== oplus strings AppSwitch ==="
$ff = Join-Path $base "follow-finger-20261106"
Get-ChildItem -LiteralPath $ff -Filter "*string*" -File | ForEach-Object {
  Write-Output ("FILE " + $_.Name)
  Select-String -LiteralPath $_.FullName -Pattern "AppSwitch|BoostType|High input|latch|InputDispatcher" | Select-Object -First 20
}
Write-Output "=== extreme-high-config-hunt ==="
Get-Content -LiteralPath (Join-Path $ff "extreme-high-config-hunt.txt") -TotalCount 80 -ErrorAction SilentlyContinue
Write-Output "=== flash bake notes ==="
Get-ChildItem -LiteralPath "$base\flash-candidate" -File | Select-Object Name,Length
Test-Path -LiteralPath "$base\donor-images\my_product.img"
# list my_product tree refresh
Get-ChildItem -LiteralPath "$base\donor-tree\my_product\etc" -ErrorAction SilentlyContinue | Where-Object { $_.Name -match "refresh|vrr|frame|screen" } | Format-Table Name,Length
