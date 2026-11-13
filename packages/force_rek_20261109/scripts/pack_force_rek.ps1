$ErrorActionPreference = "Stop"
$diag = "E:\youxikaifa\work\today-20261109\boot-diag"
$tools = "E:\youxikaifa\work\today-20261109\kb-vintf-magisk\magisk30.7-tools"
$unpack = Join-Path $diag "force-rek-unpack"
New-Item -ItemType Directory -Force -Path $unpack | Out-Null
New-Item -ItemType Directory -Force -Path $diag | Out-Null

if (-not (Test-Path (Join-Path $diag "force-rek-Image"))) {
  Copy-Item "\\wsl$\TB371FC-Builder\work\r108-out\arch\arm64\boot\Image" (Join-Path $diag "force-rek-Image") -Force
}
if (-not (Test-Path (Join-Path $diag "force-rek-base-r108.img"))) {
  Copy-Item "\\wsl$\TB371FC-Builder\work\r108-pack\boot-r108-resx.img" (Join-Path $diag "force-rek-base-r108.img") -Force
}

Get-ChildItem $unpack -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item (Join-Path $diag "force-rek-base-r108.img") (Join-Path $unpack "base.img") -Force

Push-Location $unpack
& "$tools\magiskboot" unpack base.img
if ($LASTEXITCODE -ne 0) { throw "magiskboot unpack failed: $LASTEXITCODE" }
Get-ChildItem | Format-Table Name,Length
Copy-Item (Join-Path $diag "force-rek-Image") (Join-Path $unpack "kernel") -Force
& "$tools\magiskboot" repack base.img (Join-Path $diag "boot-r108-force-rek.img")
if ($LASTEXITCODE -ne 0) { throw "magiskboot repack failed: $LASTEXITCODE" }
Pop-Location

$stock = Get-FileHash (Join-Path $diag "boot-r108-force-rek.img") -Algorithm SHA256
Write-Host ("STOCK_BOOT_SHA256=" + $stock.Hash)
Write-Host ("STOCK_BOOT_SIZE=" + (Get-Item (Join-Path $diag "boot-r108-force-rek.img")).Length)

$magiskOut = Join-Path $diag "boot-r108-force-rek-magisk.img"
$magiskBase = "E:\youxikaifa\work\today-20261109\kb-vintf-magisk\boot-r108-resx-magisk.img"
$munpack = Join-Path $diag "force-rek-magisk-unpack"
New-Item -ItemType Directory -Force -Path $munpack | Out-Null
Get-ChildItem $munpack -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item $magiskBase (Join-Path $munpack "base.img") -Force
Push-Location $munpack
& "$tools\magiskboot" unpack base.img
if ($LASTEXITCODE -ne 0) { throw "magisk unpack failed" }
Copy-Item (Join-Path $diag "force-rek-Image") (Join-Path $munpack "kernel") -Force
& "$tools\magiskboot" repack base.img $magiskOut
if ($LASTEXITCODE -ne 0) { throw "magisk repack failed" }
Pop-Location
$mh = Get-FileHash $magiskOut -Algorithm SHA256
Write-Host ("MAGISK_BOOT_SHA256=" + $mh.Hash)
Write-Host ("MAGISK_BOOT_SIZE=" + (Get-Item $magiskOut).Length)
Write-Host "DONE"
