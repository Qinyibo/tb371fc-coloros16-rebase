# BAKE-IN ABA PASS — 2026-11-06

## Result
- Magisk live MD5 = module MD5 = `35db38f8c85758c372546c707513642c`
- `Current Version:20260107` (full Config parse, not BOM fallback)
- `mDefaultRateId=[4, 4, 2, 4]`
- `mPanelRateData.PreferredRefreshRateId=[4, 4, 2, 4]` (from systemui NotificationShade_controlPanel)
- `control panel:4`
- Foreground PickRate after warm start: WeChat / Douyin / Luna = **144**
- `hardware_success_claimed=false` (Magisk trial; ROM bake-in not yet flashed into my_product image)

## Canonical XML (do not invent attrs)
```xml
<item package="com.android.systemui" rateId="4-4-2-4" animBoost="true" />
<item package="com.android.systemui" activity="NotificationShade_controlPanel" rateId="4-4-2-4" animBoost="true" />
<config … maxrefreshsettings="4" defaultMaxRate="144" defaultRateId="4-4-2-4" extremeHighEnable="true" …/>
```
- `defaultRateId` MUST be hyphen tuple `4-4-2-4` (scalar `"4"` → `[4,0,0,0]`)
- No real XML attrs: `maxRefreshRateId`, `support144Hz`, config-level `preferredRefreshRate`
- Magisk: bind **XML only**; never bind `oplus-services.jar` (bootloop)

## Paths
- Bake-in XML: `…/display-refresh-system-v4/bake-in/refresh_rate_config.xml`
- Magisk module: `…/display-refresh-system-v4/magisk-module/`
- Reverse notes: `…/RATE-TABLE-REVERSE.md`
- Dumps: `D:/TB371FC-release/clean-rebase-20261104/follow-finger-20261106/aba-bake-in.txt` + `bake-*.txt`

## Next (long-term)
1. ROM bake-in: replace stock `my_product/etc/refresh_rate_config.xml` with bake-in XML in image build (remove Magisk when verified)
2. Fluency: AppSwitchBoost / NVT touch / SF High input latency under multi third-party warm interrupt
