$ErrorActionPreference = "Stop"
$base = "D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\dynframe-144-trial"
$work = Join-Path $base "work"
New-Item -ItemType Directory -Force -Path $work | Out-Null
$rawPath = Join-Path $work "sys_dynamic_frame_config.stock.xml"
$patPath = Join-Path $work "sys_dynamic_frame_config.144.xml"
$py = "D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\_patch_dynframe.py"

if (Test-Path $rawPath) { Remove-Item $rawPath -Force }
adb pull /my_product/etc/sys_dynamic_frame_config.xml $rawPath
python $py $rawPath $patPath

$mod = Join-Path $base "magisk-module"
New-Item -ItemType Directory -Force -Path (Join-Path $mod "my_product\etc") | Out-Null
Copy-Item -LiteralPath $patPath -Destination (Join-Path $mod "my_product\etc\sys_dynamic_frame_config.xml") -Force

Set-Content -LiteralPath (Join-Path $mod "module.prop") -Encoding ascii -Value @"
id=tb371fc_dynframe_144
name=TB371FC dynframe targetFramerate 144 trial
version=v1
versionCode=1
author=tibo-sys6
description=Bind sys_dynamic_frame_config.xml targetFramerate 120->144. Reversible. Not ART/GC/OEM.
"@

$pfs = "#!/system/bin/sh`nMODDIR=`${0%/*}`nTARGET=/my_product/etc/sys_dynamic_frame_config.xml`nSRC=`$MODDIR/my_product/etc/sys_dynamic_frame_config.xml`nif [ -f `"`$SRC`" ]; then`n  mount --bind `"`$SRC`" `"`$TARGET`"`nfi`n"
[System.IO.File]::WriteAllText((Join-Path $mod "post-fs-data.sh"), $pfs, (New-Object System.Text.UTF8Encoding $false))

$donorUpd = "D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\display-refresh-system-v4\product-config\magisk-module\META-INF\com\google\android"
New-Item -ItemType Directory -Force -Path (Join-Path $mod "META-INF\com\google\android") | Out-Null
Copy-Item (Join-Path $donorUpd "update-binary") (Join-Path $mod "META-INF\com\google\android\update-binary") -Force
Copy-Item (Join-Path $donorUpd "updater-script") (Join-Path $mod "META-INF\com\google\android\updater-script") -Force

$zip = Join-Path $base "tb371fc_dynframe_144-trial.zip"
if (Test-Path $zip) { Remove-Item $zip -Force }
Push-Location $mod
jar -cfM $zip module.prop post-fs-data.sh META-INF my_product
Pop-Location

$stockMd5 = (Get-FileHash $rawPath -Algorithm MD5).Hash.ToLower()
$patchMd5 = (Get-FileHash $patPath -Algorithm MD5).Hash.ToLower()
$brief = @"
# dynframe 144 trial — Magisk (sys6)

## Why (evidence 2026-11-06 Asia/Hong_Kong)
- Panel/SF already 144: mCurrentPickRate=144, mActiveSfDisplayMode=144, mActiveRenderFrameRate=144
- Live sys_dynamic_frame_config.xml: 89x targetFramerate=120, 0x 144
- DynamicFrameRate/OverScroller/window-anim paces 120 while vsync 144 → High input latency / 跟手差
- Baseline High input latency (unlocked warm): Douyin 593 / Luna 1082 / WeChat 155
- AppSwitchBoost=true Type=0 already on (secondary)

## Artifact
- Zip: $zip
- Stock MD5: $stockMd5 (device expect 910955b13710e2174b88f45506972467)
- Patched MD5: $patchMd5

## Deploy (Codex one-shot)
1. adb push `"$zip`" /data/local/tmp/
2. adb shell su -c 'magisk --install-module /data/local/tmp/tb371fc_dynframe_144-trial.zip'
3. reboot
4. adb shell su -c 'md5sum /my_product/etc/sys_dynamic_frame_config.xml' == $patchMd5
5. Acceptance: WeChat/Douyin/Luna already open; warm am start only; NO force-stop; subjective + gfxinfo

## Rollback
Disable/remove Magisk module tb371fc_dynframe_144 → reboot

## Do NOT
- ART/GC/OEM stack; oplus-services.jar bind; per-app rateId Magisk glue

hardware_success_claimed=false
"@
[System.IO.File]::WriteAllText((Join-Path $base "TRIAL.md"), $brief, (New-Object System.Text.UTF8Encoding $false))
Write-Output "DONE stock=$stockMd5 patch=$patchMd5 zip=$zip"
Get-Item $zip | Format-List FullName,Length
