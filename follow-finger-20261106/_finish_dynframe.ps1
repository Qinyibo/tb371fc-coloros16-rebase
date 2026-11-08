$ErrorActionPreference = "Stop"
$base = "D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\dynframe-144-trial"
$mod = Join-Path $base "magisk-module"
$work = Join-Path $base "work"
$patPath = Join-Path $work "sys_dynamic_frame_config.144.xml"
$rawPath = Join-Path $work "sys_dynamic_frame_config.stock.xml"
$zip = Join-Path $base "tb371fc_dynframe_144-trial.zip"
$pyZip = "D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\_zip_magisk.py"

Copy-Item -LiteralPath $patPath -Destination (Join-Path $mod "my_product\etc\sys_dynamic_frame_config.xml") -Force
python $pyZip $mod $zip

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
- Stock MD5: $stockMd5
- Patched MD5: $patchMd5

## Deploy (Codex one-shot)
1. adb push `"$zip`" /data/local/tmp/
2. adb shell su -c 'magisk --install-module /data/local/tmp/tb371fc_dynframe_144-trial.zip'
3. reboot
4. adb shell su -c 'md5sum /my_product/etc/sys_dynamic_frame_config.xml' == $patchMd5
5. Acceptance: WeChat/Douyin/Luna already open; warm am start only; NO force-stop; subjective + gfxinfo

## Rollback
Disable/remove Magisk module tb371fc_dynframe_144 → reboot → MD5 $stockMd5

## Do NOT
- ART/GC/OEM stack; oplus-services.jar bind; per-app rateId Magisk glue

hardware_success_claimed=false
"@
[System.IO.File]::WriteAllText((Join-Path $base "TRIAL.md"), $brief, (New-Object System.Text.UTF8Encoding $false))

# sync FLUENCY brief patched md5
$flu = "D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\FLUENCY-144-NEXT.md"
if (Test-Path $flu) {
  $t = [System.IO.File]::ReadAllText($flu)
  # append exact patched md5 note
  $t2 = $t + "`r`n`r`n## Exact trial hashes (rebuilt)`r`n- stock: $stockMd5`r`n- patched: $patchMd5`r`n- zip: $zip`r`n"
  [System.IO.File]::WriteAllText($flu, $t2, (New-Object System.Text.UTF8Encoding $false))
}
Write-Output "DONE stock=$stockMd5 patch=$patchMd5"
Get-Item $zip | Format-List FullName,Length
