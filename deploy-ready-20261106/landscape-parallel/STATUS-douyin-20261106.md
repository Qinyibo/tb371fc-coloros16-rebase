# Douyin landscape / MagicWindow fix — 2026-11-06

**Device:** TB371FC ColorOS16 (Qin)
**Time:** 2026-11-06 ~20:21 Asia/Hong_Kong (UTC+8)
**Package:** `com.ss.android.ugc.aweme` (抖音 41.0.0)
**hardware_success_claimed:** false
**Untouched:** T2/refresh/pen/luna/PC WPS/interconnect

---

## Root cause

Not the earlier trim (pscanvas/cosa already re-enabled).

FantasyWindow DB (`/data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db`) had:

| field | before | meaning |
|-------|--------|---------|
| `use_function` | magicwindow | 平行视界 / Magic Window |
| `status` | **2** | disabled for this device policy |
| `config` | `{"mode":"1","excludeDevice":"PAD"}` | **explicitly excluded on PAD** |

Compare WeChat (`com.tencent.mm`) magicwindow `status=1` (works). Douyin was OEM-excluded on tablet, so it fell back to phone `SCREEN_ORIENTATION_PORTRAIT` and rotated the whole display to portrait.

`accelerometer_rotation=1`, `ignoreOrientationRequest=true` were already OK — not the blocker.

---

## Fix applied

1. Backup: `landscape-parallel/probe/fantasywindow.db.bak`
2. Patch row: `status=1`, `config={"mode":"1"}` (removed `excludeDevice:PAD`)
3. Write via Magisk `su -t <exsystemservice_pid>` (needed for `system_app_data_file` write)
4. `kill -9` exsystemservice (respawned), force-stop + relaunch Douyin

### After (verified)

- Task mode: **`oplus-magic-windows`**
- Display: **`ROTATION_90` (landscape)** while Douyin focused
- Douyin bounds in magic-window pane (not fullscreen portrait takeover)
- SF T2 still `mWorkDuration=6.94`

Note: activity still reports `requestedOrientation=PORTRAIT` inside the magic-window pane — normal for phone apps in 平行视界; the tablet stays landscape with dual/magic layout.

---

## Manual toggle (if user needs)

1. 设置 → 搜索「平行视界」→ open `com.oplus.pscanvas` SettingActivity
2. Find 抖音 and enable
3. Or: 设置 → 应用横屏显示 (`AppLandscapeModeActivity`)

If FantasyWindow cloud sync resets `excludeDevice:PAD`, re-run patch or toggle in UI.

## Rollback

```bat
adb push landscape-parallel\probe\fantasywindow.db.bak /sdcard/Download/
adb shell su -t $(pidof com.oplus.exsystemservice) -c "cp -f /sdcard/Download/fantasywindow.db.bak /data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db"
adb shell su -t $(pidof com.oplus.exsystemservice) -c "kill -9 $(pidof com.oplus.exsystemservice)"
```

## Scripts / artifacts

- `probe/fantasywindow.db.bak` — pre-fix
- `probe/fantasywindow.patched.db` / `fantasywindow.after.db`
- `probe/patch_fw.py`, `verify_fw.py`
