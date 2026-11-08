#!/system/bin/sh
ls /data/user/0/com.tencent.mobileqq/shared_prefs/ | head -80
grep -RIl -E "pad|tablet|Pad|PAD|dual|split|landscape|平板" /data/user/0/com.tencent.mobileqq/shared_prefs/ 2>/dev/null | head -30