#!/system/bin/sh
grep -RIl -E "PadMode|pad_mode|tablet_mode|isPad|AIO_PAD|Conversation.*Pad|splitAIO|dual_pane|PadAIO|use_pad" /data/user/0/com.tencent.mobileqq/ 2>/dev/null | head -40
grep -RhoE ".{0,40}(PadMode|pad_mode|isPad|AIO_PAD|dual).{0,40}" /data/user/0/com.tencent.mobileqq/shared_prefs/ 2>/dev/null | head -40