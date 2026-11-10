# REQUIRES explicit operator approval before running.
# Flashes Magisk-patched r108 boot, installs VINTF module, one reboot, verifies.
# Keyboard UNPLUGGED. No remount /vendor. No vbmeta change.
param(
  [switch]$DoFlash,
  [switch]$DoInstallModule
)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$PatchedBoot = Join-Path $Root "boot-r108-resx-magisk.img"
$StockBoot   = "E:\youxikaifa\work\today-20261109\boot-r108-resx.img"
$ModuleZip   = Join-Path $Root "tb371fc_tinno_vintf_pair.zip"
$ExpectPatched = "62428F25F857BCC15FE8AB4A3A18148C5B37723109DE60F974C470188839A825"
$ExpectStock   = "F5F446047721E788451FBDE8D984A8E3DCA0AC21E18E85F9F15839C6289B1F13"
$ExpectZip     = "16E3F4FF045D824482EFCD5CE92251129A8FCB2326F38BC36978AD6CF3AB2078"

function Assert-Sha($path, $expect) {
  $h = (Get-FileHash $path -Algorithm SHA256).Hash.ToUpperInvariant()
  if ($h -ne $expect.ToUpperInvariant()) { throw "SHA mismatch $path got=$h expect=$expect" }
  Write-Host "OK SHA256 $path"
}

Assert-Sha $PatchedBoot $ExpectPatched
Assert-Sha $StockBoot $ExpectStock
Assert-Sha $ModuleZip $ExpectZip

if (-not $DoFlash) {
  Write-Host "DRY RUN only. Re-run with -DoFlash to flash boot_a + reboot."
  Write-Host "After Magisk is up, re-run with -DoFlash -DoInstallModule OR just install module step carefully."
  exit 0
}

Write-Host "=== FLASH boot_a with Magisk 30.7 patched r108 (KEEPVERITY=true) ==="
adb reboot bootloader
Start-Sleep -Seconds 8
fastboot devices
fastboot flash boot_a $PatchedBoot
fastboot set_active a
fastboot reboot
Write-Host "Waiting for adb device..."
adb wait-for-device
$deadline = (Get-Date).AddMinutes(5)
do {
  Start-Sleep -Seconds 3
  $bc = (adb shell getprop sys.boot_completed 2>$null | Out-String).Trim()
  Write-Host "boot_completed=$bc"
} while (($bc -ne "1") -and ((Get-Date) -lt $deadline))

if ($DoInstallModule) {
  Write-Host "=== INSTALL Magisk module ==="
  adb push $ModuleZip /data/local/tmp/tb371fc_tinno_vintf_pair.zip
  adb shell "su -c 'magisk --install-module /data/local/tmp/tb371fc_tinno_vintf_pair.zip'"
  adb reboot
  adb wait-for-device
  $deadline = (Get-Date).AddMinutes(5)
  do {
    Start-Sleep -Seconds 3
    $bc = (adb shell getprop sys.boot_completed 2>$null | Out-String).Trim()
  } while (($bc -ne "1") -and ((Get-Date) -lt $deadline))
  Write-Host "=== VERIFY ==="
  adb shell "getprop init.svc.tinnokeyboard; getprop ro.build.display.id"
  adb shell "su -c 'grep -n tinno /vendor/etc/vintf/compatibility_matrix.xml'"
  adb shell "su -c 'ls -l /vendor/etc/vintf/manifest/*tinno* 2>/dev/null; ls -l /data/adb/modules/tb371fc_tinno_vintf_pair'"
}

Write-Host "ROLLBACK: fastboot flash boot_a $StockBoot ; fastboot set_active a ; fastboot reboot"