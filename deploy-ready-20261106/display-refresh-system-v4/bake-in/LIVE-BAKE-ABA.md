# LIVE-BAKE-ABA — TB371FC ColorOS16 refresh XML system-tree bake

- Timestamp (Qin local / Asia/Hong_Kong): 2026-11-06 16:34:02
- Device: HA1W0JA3 TB371FC OPD2413_16.0.10.600(CN01) slot=_a
- Method: **A-live** remount+write /my_product/etc/refresh_rate_config.xml on system_a (dm-2)
- Flashed: **NO** (ignored `my_product-bakein.img`; no `my_product` partition)
- hardware_success_claimed: **false** (subjective fluency not separately accepted)
- refresh long-term bake ABA: **PASS**

## Pre → Post MD5

| Stage | Path / context | MD5 |
|-------|----------------|-----|
| Stock (after `su -mm` umount Magisk bind) | system-tree `/my_product/etc/refresh_rate_config.xml` | `7e48f867e573a1e207471805e3d03902` |
| Bake-in XML (host + pushed) | `D:\...\bake-in\refresh_rate_config.xml` / `/data/local/tmp/...` | `35db38f8c85758c372546c707513642c` |
| After write (pre-reboot) | system-tree target, Magisk bind gone | `35db38f8c85758c372546c707513642c` |
| After reboot ABA | same path, **NO Magisk bind** | `35db38f8c85758c372546c707513642c` |

Stock backup:
- Device: `/data/local/tmp/refresh_rate_config.xml.stock-20261106-163036` (size 200296)
- Host: `D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\display-refresh-system-v4\bake-in\refresh_rate_config.xml.stock-20261106-163036` (MD5 `7e48f867…`)

## Magisk

| Item | Result |
|------|--------|
| Module `tb371fc_system_refresh_policy` v4d | **disabled** via `touch .../disable` (file present after reboot; mtime 2026-11-06 16:30) |
| Bind `sda15 → /my_product/etc/refresh_rate_config.xml` | **NONE** after umount + after reboot |
| `tb371fc_luna_heap_offset_fix` | **untouched** (still listed under `/data/adb/modules/`) |
| Other modules present | dynframe_144, sf_duration_144, vrr_touchidle_off (not modified this turn) |

## ABA dumpsys oplusscreenmode (post-reboot, Magisk refresh disabled)

Key lines observed:

```
Current Version:20260107
Config{ ... mMaxRefreshSettings=4 ... mDefaultRateId=[4, 4, 2, 4] mDefaultMaxRate=144.0 ... }
mPanelRateData = RateData{PreferredRefreshRateData{mPreferredRefreshRateId=[4, 4, 2, 4],isAnimBoost=true}}
mCurrentPickMode=4
mCurrentPickRate=144.00002
mSupportMaxRefreshRate=144.0
```

Settings:
- `oplus_customize_screen_refresh_rate=4` (control panel:4)
- `peak_refresh_rate=144.00002`

Warm apps (monkey launch; PickRate all 144.00002):
- WeChat `com.tencent.mm` → mCurrentPickRate=144.00002
- Douyin `com.ss.android.ugc.aweme` → mCurrentPickRate=144.00002
- Luna `com.luna.music` → mCurrentPickRate=144.00002

## Procedure executed

1. Rewrote `live-bake-refresh-xml.sh` with stock backup, MD5 gate, remount rw/ro, Magisk disable.
2. `adb push` XML + script → `/data/local/tmp/`.
3. `su -mm -c 'sh /data/local/tmp/live-bake-refresh-xml.sh'`:
   - umount Magisk bind → underlying stock `7e48…`
   - backup stock → remount rw → cp bake-in → restorecon → sync → remount ro
   - written MD5 `35db…` verified
   - `touch /data/adb/modules/tb371fc_system_refresh_policy/disable`
4. Pulled stock backup to bake-in folder on D:.
5. Reboot; boot_completed ~16:31:28 Qin local.
6. ABA as above → **PASS**.

Script run log: `D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\display-refresh-system-v4\bake-in\live-bake-run-20261106.log`

## Rollback (if needed)

Re-enable Magisk bind only:
```
adb -s HA1W0JA3 shell su -c 'rm -f /data/adb/modules/tb371fc_system_refresh_policy/disable'
adb -s HA1W0JA3 reboot
```

Or restore stock XML then Magisk:
```
adb -s HA1W0JA3 push "D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\display-refresh-system-v4\bake-in\refresh_rate_config.xml.stock-20261106-163036" /data/local/tmp/refresh_rate_config.stock.xml
adb -s HA1W0JA3 shell su -mm -c "mount -o remount,rw /; cp -f /data/local/tmp/refresh_rate_config.stock.xml /my_product/etc/refresh_rate_config.xml; chmod 644 /my_product/etc/refresh_rate_config.xml; chown root:root /my_product/etc/refresh_rate_config.xml; restorecon -v /my_product/etc/refresh_rate_config.xml; sync; mount -o remount,ro /; rm -f /data/adb/modules/tb371fc_system_refresh_policy/disable"
adb -s HA1W0JA3 reboot
```

## Notes / stderr

- `restorecon` printed SELinux file_contexts load lines to stderr (non-fatal); bake exit 0.
- `my_product-bakein.img` remains on disk as wrong-target artifact — **do not flash**.
- Subjective follow-finger fluency still needs human acceptance → `hardware_success_claimed=false`.