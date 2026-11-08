#!/system/bin/sh
# tb371fc_sf_duration_donor_loose — donor LOOSE only; NOT hang tight recipe
resetprop debug.sf.use_phase_offsets_as_durations 1
resetprop debug.sf.late.app.duration 13666666
resetprop debug.sf.early.app.duration 13666666
resetprop debug.sf.earlyGl.app.duration 13666666
resetprop debug.sf.late.sf.duration 10500000
resetprop debug.sf.early.sf.duration 10500000
resetprop debug.sf.earlyGl.sf.duration 10500000
# neutralize live high_fps phase so flag=1 does not treat -4000000/1000000 as durations
resetprop debug.sf.high_fps_late_app_phase_offset_ns 13666666
resetprop debug.sf.high_fps_early_phase_offset_ns 13666666
resetprop debug.sf.high_fps_late_sf_phase_offset_ns 10500000
resetprop debug.sf.high_fps_early_gl_phase_offset_ns 10500000
resetprop debug.sf.enable_advanced_sf_phase_offset 1