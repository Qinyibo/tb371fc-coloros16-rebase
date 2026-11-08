# ABA v4 clean product config (2026-11-06)

## Result: PASS for system PickRate/SF 144 WITHOUT framework jar patch

### What worked
- Magisk module `tb371fc_system_refresh_policy` v4
- refresh_rate_config.xml: maxrefreshsettings=4 defaultMaxRate=144 extremeHighEnable=true
- **NO** defaultRateId / maxRefreshRateId attributes (those made mDefaultRateId=[4,0,0,0] and fought the path)
- no-BOM UTF-8
- Live: Version=20260107, Config MaxRefreshSettings=4 DefaultMaxRate=144 ExtremeHighEnable=true
- mCurrentPickMode=4 mCurrentDefaultRateId=4 mCurrentPickRate=144
- SF activeMode/renderRate=144 Hz; settings peak_refresh_rate=144; oplus_customize_screen_refresh_rate=4

### What failed / must not ship
- Magisk bind of patched `oplus-services.jar` (getSettingModeIndex 3→7) → **bootanim hang / soft brick risk**. Module marked remove. Index-cap only via signed ROM bake-in if still needed later.
- Magisk zip CreateFromDirectory on Windows dropped nested entries; use adb push into /data/adb/modules/ or zip with Unix attrs.

### Remaining (not done = not long-term done)
- mPanelRateData PreferredRefreshRateId still [3,2,2,3] (120-centric); control panel:3 can vote 120
- AppSwitchBoost may still clamp interrupt path to 120
- Magisk trial ≠ ROM bake-in
- Fluency/touch High input latency under multi third-party warm interrupt
- hardware_success_claimed=false

### Next execute
1. Reboot ABA: confirm post-fs-data bind survives (chmod 755)
2. Fix PreferredRefreshRate table / rate-id policy at product XML (system layer, not per-app list)
3. AppSwitchBoost path
4. Bake product XML into my_product for ROM
