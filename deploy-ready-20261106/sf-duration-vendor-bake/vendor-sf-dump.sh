#!/system/bin/sh
dumpsys SurfaceFlinger > /data/local/tmp/sf-after-donor-loose.txt
grep -n -E 'mWorkDuration|mReadyDuration|PhaseOffsets|appDuration|sfDuration|usePhaseOffsetsAsDurations|high_fps|144.00|refresh-rate|Default|Preferred' /data/local/tmp/sf-after-donor-loose.txt | head -80
echo ====
getprop | grep -E 'debug.sf.' | sort
