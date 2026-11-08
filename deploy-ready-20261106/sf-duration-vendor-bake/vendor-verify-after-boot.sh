#!/system/bin/sh
echo ==== BOOT ====
getprop sys.boot_completed
getprop ro.build.display.id
getprop ro.boot.slot_suffix
echo ==== PROP DURATION ====
getprop debug.sf.use_phase_offsets_as_durations
getprop debug.sf.late.app.duration
getprop debug.sf.early.app.duration
getprop debug.sf.earlyGl.app.duration
getprop debug.sf.late.sf.duration
getprop debug.sf.early.sf.duration
getprop debug.sf.earlyGl.sf.duration
getprop debug.sf.enable_advanced_sf_phase_offset
echo ==== PROP HIGH_FPS ====
getprop debug.sf.high_fps_late_app_phase_offset_ns
getprop debug.sf.high_fps_late_sf_phase_offset_ns
getprop debug.sf.high_fps_early_phase_offset_ns
getprop debug.sf.high_fps_early_gl_phase_offset_ns
echo ==== FILE ====
md5sum /vendor/build.prop
grep -E 'high_fps|duration|use_phase|enable_advanced_sf' /vendor/build.prop
echo ==== REFRESH ====
md5sum /my_product/etc/refresh_rate_config.xml
echo ==== SF DUMP ====
dumpsys SurfaceFlinger | grep -E 'mWorkDuration|mReadyDuration|peak-refresh-rate|activeMode|appDuration|sfDuration|PhaseOffsets|usePhaseOffsetsAsDurations' | head -40
echo ==== MAGISK ====
ls /data/adb/modules/tb371fc_sf_duration_144/disable /data/adb/modules/tb371fc_sf_duration_donor_loose/disable /data/adb/modules/tb371fc_dynframe_144/disable /data/adb/modules/tb371fc_vrr_touchidle_off/disable /data/adb/modules/tb371fc_system_refresh_policy/disable 2>&1
ls /data/adb/modules/tb371fc_luna_heap_offset_fix/disable 2>&1 || echo luna_no_disable_file
echo ==== FLAG ====
ls -l /data/local/tmp/vendor_prop_trial.flag 2>&1
