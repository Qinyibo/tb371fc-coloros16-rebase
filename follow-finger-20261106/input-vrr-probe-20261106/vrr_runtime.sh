#!/system/bin/sh
echo MD5_PRODUCT
md5sum /my_product/etc/oplus_vrr_config.json
echo MD5_DATA
md5sum /data/system/oplus_vrr_config.json 2>/dev/null || echo none
ls -la /data/system/oplus_vrr_config.json 2>/dev/null || true
echo ===RUNTIME===
dumpsys oplus_vrr_service | grep -iE 'TouchIdle|CurrentMode|VrrState|Frtc switch|OtiHigh|m144|SwWhite|CurrPkg|ModeId|TouchFrame'
echo ===SF_DUR===
dumpsys SurfaceFlinger | grep -iE 'WorkDuration|ReadyDuration|renderRate|activeMode|touchTimer'
echo ===IRQ===
grep NVT /proc/interrupts
