# dynframe 144 trial 鈥?Magisk (sys6)

## Why (evidence 2026-11-06 Asia/Hong_Kong)
- Panel/SF already 144: mCurrentPickRate=144, mActiveSfDisplayMode=144, mActiveRenderFrameRate=144
- Live sys_dynamic_frame_config.xml: 89x targetFramerate=120, 0x 144
- DynamicFrameRate/OverScroller/window-anim paces 120 while vsync 144 鈫?High input latency / 璺熸墜宸?- Baseline High input latency (unlocked warm): Douyin 593 / Luna 1082 / WeChat 155
- AppSwitchBoost=true Type=0 already on (secondary)

## Artifact
- Zip: D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\dynframe-144-trial\tb371fc_dynframe_144-trial.zip
- Stock MD5: 910955b13710e2174b88f45506972467
- Patched MD5: fb92391a1a6a5c3486268a41aa95bc63

## Deploy (Codex one-shot)
1. adb push "D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\dynframe-144-trial\tb371fc_dynframe_144-trial.zip" /data/local/tmp/
2. adb shell su -c 'magisk --install-module /data/local/tmp/tb371fc_dynframe_144-trial.zip'
3. reboot
4. adb shell su -c 'md5sum /my_product/etc/sys_dynamic_frame_config.xml' == fb92391a1a6a5c3486268a41aa95bc63
5. Acceptance: WeChat/Douyin/Luna already open; warm am start only; NO force-stop; subjective + gfxinfo

## Rollback
Disable/remove Magisk module tb371fc_dynframe_144 鈫?reboot 鈫?MD5 910955b13710e2174b88f45506972467

## Do NOT
- ART/GC/OEM stack; oplus-services.jar bind; per-app rateId Magisk glue

hardware_success_claimed=false