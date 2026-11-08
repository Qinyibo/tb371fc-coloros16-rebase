$ErrorActionPreference = "Stop"
$base = "D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106"
$ff = "D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106"
$probe = Get-ChildItem -LiteralPath $ff -Directory | Where-Object { $_.Name -like "dynframe-probe-*" } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $probe) { throw "no dynframe-probe dir" }
$live = Join-Path $probe.FullName "sys_dynamic_frame_config.live.xml"
if (-not (Test-Path -LiteralPath $live)) { throw "missing live xml" }

$outRoot = Join-Path $base "dynframe-144-trial"
$mod = Join-Path $outRoot "magisk-module"
New-Item -ItemType Directory -Force -Path (Join-Path $mod "my_product\etc") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $mod "META-INF\com\google\android") | Out-Null

$raw = [System.IO.File]::ReadAllText($live)
$orig120 = ([regex]::Matches($raw, 'targetFramerate="120"')).Count
$patched = $raw.Replace('targetFramerate="120"', 'targetFramerate="144"')
$now144 = ([regex]::Matches($patched, 'targetFramerate="144"')).Count
$still120 = ([regex]::Matches($patched, 'targetFramerate="120"')).Count

$dstXml = Join-Path $mod "my_product\etc\sys_dynamic_frame_config.xml"
# write UTF-8 no BOM
$utf8 = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($dstXml, $patched, $utf8)

$md5 = (Get-FileHash -LiteralPath $dstXml -Algorithm MD5).Hash.ToLower()
$liveMd5 = (Get-FileHash -LiteralPath $live -Algorithm MD5).Hash.ToLower()

@"
id=tb371fc_dynframe_144
name=TB371FC dynframe targetFramerate 144 trial
version=v1
versionCode=1
author=tibo-sys6
description=Bind my_product/etc/sys_dynamic_frame_config.xml with targetFramerate 120->144 (scroll/anim path). Reversible Magisk. Not ART/GC/OEM.
"@ | Set-Content -LiteralPath (Join-Path $mod "module.prop") -Encoding ascii

@"
#!/system/bin/sh
# Magisk module: bind dynframe config only
MODDIR=`${0%/*}
TARGET=/my_product/etc/sys_dynamic_frame_config.xml
SRC=`$MODDIR/my_product/etc/sys_dynamic_frame_config.xml
if [ -f "`$SRC" ]; then
  mount --bind "`$SRC" "`$TARGET"
fi
"@ | Set-Content -LiteralPath (Join-Path $mod "post-fs-data.sh") -Encoding ascii

# updater-script / update-binary stubs (copy from existing refresh module if present)
$donorUpd = Join-Path $base "display-refresh-system-v4\product-config\magisk-module\META-INF\com\google\android"
if (Test-Path -LiteralPath $donorUpd) {
  Copy-Item -LiteralPath (Join-Path $donorUpd "update-binary") -Destination (Join-Path $mod "META-INF\com\google\android\update-binary") -Force
  Copy-Item -LiteralPath (Join-Path $donorUpd "updater-script") -Destination (Join-Path $mod "META-INF\com\google\android\updater-script") -Force
}

# zip
$zip = Join-Path $outRoot "tb371fc_dynframe_144-trial.zip"
if (Test-Path -LiteralPath $zip) { Remove-Item -LiteralPath $zip -Force }
Compress-Archive -Path (Join-Path $mod '*') -DestinationPath ($zip + ".tmp.zip") -Force
Move-Item -LiteralPath ($zip + ".tmp.zip") -Destination $zip -Force

# brief
$brief = @"
# dynframe 144 trial — Magisk (sys6)

## Why
Live panel/SF PickRate=144 but `/my_product/etc/sys_dynamic_frame_config.xml` still has **$orig120** `targetFramerate="120"` and **0** `targetFramerate="144"`.
Oplus DynamicFrameRate / OverScroller / window anim path therefore paces at 120 while display vsync is 144 → High input latency / 跟手差 under warm multi-app interrupt.

## What changed
- Replace every `targetFramerate="120"` → `"144"` in product dynframe XML.
- Patched count: targetFramerate=144 → $now144 ; remaining 120 → $still120
- Live stock MD5: $liveMd5
- Patched MD5: $md5

## Deploy (Codex one-shot)
1. `adb push $zip /data/local/tmp/`
2. Magisk install zip (or `su -c 'magisk --install-module /data/local/tmp/tb371fc_dynframe_144-trial.zip'`)
3. Reboot
4. Verify: `md5sum /my_product/etc/sys_dynamic_frame_config.xml` == $md5
5. Warm interrupt acceptance: WeChat/Douyin/Luna already open, `am start` only (NO force-stop); subjective 跟手 + gfxinfo High input latency

## Rollback
Disable/remove Magisk module `tb371fc_dynframe_144` → reboot → MD5 back to $liveMd5

## Constraints
- Do NOT stack ART/GC/OEM-identity
- Keep `tb371fc_system_refresh_policy` until ROM bake-in; this module is orthogonal (dynframe vs refresh_rate_config)
- hardware_success_claimed=false
"@
Set-Content -LiteralPath (Join-Path $outRoot "TRIAL.md") -Value $brief -Encoding utf8

Write-Output ("orig120=" + $orig120 + " now144=" + $now144 + " still120=" + $still120)
Write-Output ("liveMd5=" + $liveMd5)
Write-Output ("patchedMd5=" + $md5)
Write-Output ("zip=" + $zip)
Get-ChildItem -LiteralPath $outRoot -Recurse | Select-Object FullName,Length | Format-Table -AutoSize
