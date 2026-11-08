#!/system/bin/sh
# tb371fc_sf_duration_144 post-fs-data
resetprop debug.sf.use_phase_offsets_as_durations 1
resetprop debug.sf.late.app.duration 6944444
resetprop debug.sf.late.sf.duration 8500000
resetprop debug.sf.early.app.duration 6944444
resetprop debug.sf.early.sf.duration 8500000
resetprop debug.sf.earlyGl.app.duration 6944444
resetprop debug.sf.earlyGl.sf.duration 8500000
resetprop debug.sf.high_fps_late_app_phase_offset_ns 6944444
resetprop debug.sf.high_fps_late_sf_phase_offset_ns 8500000
resetprop debug.sf.high_fps_early_phase_offset_ns 6944444
resetprop debug.sf.high_fps_early_gl_phase_offset_ns 8500000
resetprop debug.sf.enable_advanced_sf_phase_offset 1
