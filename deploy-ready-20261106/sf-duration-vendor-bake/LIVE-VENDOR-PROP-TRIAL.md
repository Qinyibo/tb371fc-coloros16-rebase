# LIVE-VENDOR-PROP-TRIAL.md

**时间:** 2026-11-06 Asia/Hong_Kong (~18:26–18:29)  
**hardware_success_claimed=false**  
**机:** Qin `0bc7a3ae-6c23-4ea4-bc02-c2f0075b312d` / TB371FC slot `_a`

## Outcome (one line)

**Live remount-rw of `/vendor` WORKED; donor-loose `build.prop` applied; boot OK; `mWorkDuration` 8.89 → 13.67; rollback NOT needed.**

| Question | Answer |
|----------|--------|
| remount path used? | **YES** (`mount -o remount,rw /vendor` as Magisk uid0) |
| boot ok? | **YES** — `sys.boot_completed=1` ~50s after reboot |
| new mWorkDuration? | **13.67 ms** (was 8.89); `mReadyDuration` **10.50** (was 10.94) |
| rollback done? | **NO** — hang did not occur; stock kept at `/data/local/tmp/build.prop.stock` + `/data/adb/sf_duration_rollback/` |

## Pre-flight (healthy baseline)

| Check | Result |
|-------|--------|
| `sys.boot_completed` | 1 |
| BuildId | `OPD2413_16.0.10.600(CN01)` |
| refresh XML MD5 | `35db38f8c85758c372546c707513642c` |
| SF Magisk (`sf_duration_144`, `sf_duration_donor_loose`, dynframe, vrr, refresh policy) | all have `disable` |
| Luna Magisk | enabled (no `disable`) |
| `/vendor` FS | **ext4** on `/dev/block/dm-4`, initially `ro` |
| live `build.prop` MD5 | `fe6f8d95b40efedfcdfc45cf05ba6ec7` (high_fps present, no duration) |
| baseline `mWorkDuration` | 8.89 |

## What was applied (same as offline prep)

Source: `vendor-offline-prep/build.prop.donor-loose-patched` MD5 `cfb2330f897a9d00d3f5f5fe494daf37`

- **Removed** 4× `debug.sf.high_fps_*_phase_offset_ns`
- **Inserted** after `enable_advanced_sf_phase_offset=1`:
  - `use_phase_offsets_as_durations=1`
  - app duration ×3 = `13666666`
  - sf duration ×3 = `10500000`

On-disk after apply: `/vendor/build.prop` MD5 `cfb2330f…`, mode `600`, SELinux `u:object_r:vendor_file:s0`, remounted `ro`.

## Post-boot verification

| Item | Value |
|------|-------|
| `debug.sf.use_phase_offsets_as_durations` | `1` |
| `debug.sf.*.app.duration` | `13666666` |
| `debug.sf.*.sf.duration` | `10500000` |
| `debug.sf.high_fps_*` getprop | **empty** (absent) |
| dumpsys `mWorkDuration` / `mReadyDuration` | **13.67 / 10.50** (= 13666666 / 10500000 ns) |
| vsync / peak refresh | **144.00 Hz** |
| refresh XML | still `35db38f8…` |
| SF duration Magisk | still disabled |
| Luna | still enabled |

Evidence:
- `LIVE-VENDOR-PROP-BOOTWATCH.txt`
- `LIVE-VENDOR-PROP-VERIFY.txt`
- `sf-after-donor-loose-dumpsys.txt`
- scripts: `vendor-apply-donor-loose.sh`, `vendor-restore-stock.sh`

## Why Magisk hung but remount did not

Same numeric donor-loose set. Difference:

| Path | Timing / mechanism | Result on TB371FC |
|------|--------------------|-------------------|
| Magisk `system.prop` + `resetprop` in post-fs-data | injects after early init; previous trials also rewrote/kept high_fps into duration-scale values | **BOOT HANG** (tight + loose) |
| Vendor `build.prop` remount | props loaded by init from disk at boot; high_fps **deleted** (donor topology) | **BOOT OK** |

→ Magisk duration path stays **CLOSED**. Vendor remount bake path is **OPEN** for further numeric trials (with stock restore script ready).

## Follow-finger implication (honest)

Donor-loose **does not tighten** toward 144 period (6.94 ms). It **loosens** work budget 8.89 → 13.67 (~2 frames).  
This trial proves **boot-safe vendor bake** and that duration props are live-consumed; it is **not** claimed as跟手 win.  
`hardware_success_claimed=false`.

## Rollback readiness (unused)

```
adb shell "su -c 'sh /data/local/tmp/vendor-restore-stock.sh'"
adb reboot
```

Stock MD5 target: `fe6f8d95b40efedfcdfc45cf05ba6ec7`.  
Host copy: `vendor-offline-prep/build.prop.stock-before-live-remount`.

## Fastboot note (unchanged)

Large raw `vendor_a` flash via fastbootd still unreliable (USB timeout / sparse). Prefer live remount for prop-only edits. Sparse/`img2simg` bootloader path not required for this prop trial.

## Next (suggested, not done this turn)

1. Subjective跟手 vs 8.89 baseline (may feel worse/slacker).  
2. If worse: remount-restore stock immediately.  
3. If exploring tighter budgets: only via **vendor remount** (not Magisk), step from donor-loose toward live-mapped 8888888/10944444 then cautiously below — each step with restore script staged; never re-enable Magisk duration.

## Related

- `vendor-offline-prep/README.md`
- `FLASH-VENDOR-DONOR-LOOSE-RESULT.md` (flash never completed; superseded by this live remount success)
- `DURATION-BOUNDS-20261106.md`
- `donor-loose-magisk-trial/RESULT-BOOT-HANG-ROLLED-BACK.md`