@echo off
adb shell su -c "am start -n com.android.settings/com.android.settings.SubSettings --es :settings:show_fragment com.oplus.settings.feature.display.parallel.ParallelWorldFragment --es :settings:show_fragment_title ????"
echo Opened Settings ParallelWorld list. Also try Settings search: ????
