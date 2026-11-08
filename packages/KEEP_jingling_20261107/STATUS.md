# STATUS · KEEP + 鲸鲮 Office V2.1 完整刷机包 · 2026-11-07

`hardware_success_claimed=false`

## Package COMPLETE (v27-equivalent)

PRIMARY: `D:\TB371FC-release\ColorOS16_TB371FC_KEEP_jingling_20261107_CANDIDATE\`
MIRROR: `D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\full-rom-keep-jingling\`

Contents: 1-连接检查.cmd, 2-刷前检查.cmd, 一键刷入.cmd / 一键刷入-delta.cmd / 一键刷入-完整super.cmd, 核验ROM.cmd, 刷入说明.md, STATUS.md, DEPLOY.md, SHA256SUMS.txt, manifest.json, images/(super+boot+vbmeta+vbmeta_system), tools/, scripts/, verification/, assets/, delta/

## Images
- super `9845539c7c139cc08408bbc6f9a3d9c1653c0b84821e6170993f651df73c27cb`
- boot `5b4acefcc109ece2d3b84ce646b3496de6dfe2dc4b33d459bd2557d4d9a38b3a`
- YozoOffice SHA256 `0cc7977db6c35eab3dd3e919800b06d59d0035a819f30fa464726aeb5e508461` @ `/system/app/YozoOffice/YozoOffice.apk`

## Flash-test (Asia/Hong_Kong 2026-11-07T00:42:42.130572+08:00)
- Method: `flash_candidate_delta.py` FROM `7b1c6736…` → TO `9845539c…` (19 sparse parts, Writing OKAY, reboot OKAY, wipe=false)
- Boot completed; SELinux Enforcing
- `pm path com.yozo.office` → `package:/system/app/YozoOffice/YozoOffice.apk`
- APK md5 `0ac7c74fffb04e835655a97910d833cf` / sha256 `0cc7977d…` MATCH bake
- Live refresh XML md5 currently `67a0e527…` (Magisk overlay likely; image bake still preserves `35db38f8…`)
- Magisk modules dir not listed under this su invocation; disable Magisk jingling module manually if still present to confirm pure ROM path

## Notes
- Removed `my_product/del-app/WpsLauncher` in image only to free ~862MB for Jingling bake
- Not Magisk-only package; Jingling is in flashable system image

## Encoding fix (Asia/Hong_Kong 2026-11-07)
- Root cause: Chinese-body UTF-8 `.cmd` parsed as GBK → `'瀹屾暣' / 'er' 不是内部或外部命令`
- Match v27 practice: ASCII entry points + Chinese names are thin `call` wrappers
- User should double-click: **FLASH.cmd** (recommended delta). Also: check1.cmd, check2.cmd, flash-delta.cmd, flash-full.cmd, verify.cmd
