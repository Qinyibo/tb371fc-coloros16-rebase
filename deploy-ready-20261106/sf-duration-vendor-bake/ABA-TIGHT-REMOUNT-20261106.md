# ABA-TIGHT-REMOUNT-20261106.md

**时间:** 2026-11-06 Asia/Hong_Kong (~18:30–18:35)  
**hardware_success_claimed=false**  
**机:** Qin `0bc7a3ae-6c23-4ea4-bc02-c2f0075b312d` / TB371FC slot `_a`  
**路径:** 仅 live remount-rw `/vendor` bake（**禁止 Magisk duration**）

## Outcome (one line)

**Stock rollback OK → T1 (7.50/9.00) boot OK → T2 (6.94/8.50) boot OK. Device left on T2. Magisk-hang numbers are boot-safe via remount bake.**

## Trial table

| Trial | app.duration (ns) | sf.duration (ns) | high_fps_* | Path | Boot | mWorkDuration | mReadyDuration | Notes |
|-------|-------------------|------------------|------------|------|------|---------------|----------------|-------|
| Stock (baseline after rollback) | *(absent)* | *(absent)* | present (1e6 / -4e6) | remount restore | **OK** | **8.89** | **10.94** | MD5 `fe6f8d95…` |
| Donor-loose (prior session) | 13666666 | 10500000 | removed | remount | OK | 13.67 | 10.50 | worse vs stock; rolled back this session |
| Magisk tight (prior) | 6944444 | 8500000 | rewritten to same | Magisk | **HANG** | n/a | n/a | CLOSED |
| Magisk loose (prior) | 13666666 | 10500000 | various | Magisk | **HANG** | n/a | n/a | CLOSED |
| **T1** | **7500000** | **9000000** | removed | remount | **OK** ~10s | **7.50** | **9.00** | toward 144 period |
| **T2 (FINAL on device)** | **6944444** | **8500000** | removed | remount | **OK** ~10s | **6.94** | **8.50** | =144 period; Magisk hung, remount did not |

## Step log

### 1) Rollback to stock
- Ran `/data/local/tmp/vendor-restore-stock.sh`
- `/vendor/build.prop` → MD5 `fe6f8d95b40efedfcdfc45cf05ba6ec7`
- high_fps lines restored; duration/use_phase absent
- Reboot → `boot_completed=1`
- dumpsys: `mWorkDuration=8.89 mReadyDuration=10.94`
- refresh XML MD5 unchanged: `35db38f8c85758c372546c707513642c`

### 2) T1 remount bake
- Patch: remove 4× `high_fps_*`; after `enable_advanced_sf_phase_offset=1` insert:
  - `use_phase_offsets_as_durations=1`
  - app ×3 = `7500000`
  - sf ×3 = `9000000`
- Host file: `vendor-offline-prep/build.prop.t1-7500-9000` MD5 `681684ccbc67da42b42268f7e4da11ee`
- Apply: `vendor-apply-trial.sh T1-7500-9000`
- Reboot → boot OK; Work/Ready **7.50 / 9.00**; peak 144 Hz; refresh MD5 intact
- Evidence: `T1-VERIFY.txt`, `T1-SF-DURATION.txt`

### 3) T2 remount bake (optional, taken)
- Same topology; app=`6944444` sf=`8500000` (same numbers that hung under Magisk)
- Host file: `vendor-offline-prep/build.prop.t2-6944-8500` MD5 `b5ef1471f1b6a946be98358ed853df03`
- Apply: copy → `build.prop.trial-patched` → `vendor-apply-trial.sh T2-6944-8500`
- Reboot → boot OK; Work/Ready **6.94 / 8.50**; props match; refresh MD5 intact
- Evidence: `T2-VERIFY.txt`, `T2-SF-DURATION.txt`

## Final device state (left intentionally)

| Item | Value |
|------|-------|
| `/vendor/build.prop` MD5 | `b5ef1471f1b6a946be98358ed853df03` (T2) |
| `mWorkDuration` / `mReadyDuration` | **6.94 / 8.50** |
| `use_phase_offsets_as_durations` | 1 |
| app / sf duration getprop | 6944444 / 8500000 |
| high_fps getprop | empty |
| refresh XML | `35db38f8…` kept |
| SF duration Magisk modules | still **disabled** |
| Luna Magisk | still enabled (no `disable` file) |
| BuildId / slot | `OPD2413_16.0.10.600(CN01)` / `_a` |
| `hardware_success_claimed` | **false** (dumpsys win only; no subjective跟手 claim this turn) |

## Why Magisk hung but remount T2 did not

Same numeric 6944444/8500000. Difference remains:

| Path | Mechanism | Result |
|------|-----------|--------|
| Magisk `system.prop` / `resetprop` | late inject; prior trials also rewrote high_fps into duration-scale | BOOT HANG |
| Vendor `build.prop` remount | init loads from disk at boot; high_fps **deleted** | BOOT OK @ 6.94 |

→ Magisk duration stays **CLOSED**. Remount bake path is the supported numeric trial channel.

## Rollback readiness (staged)

```
# restore stock
adb shell "su -c 'sh /data/local/tmp/vendor-restore-stock.sh'"
adb reboot

# or re-apply T1 if preferred mid-point
adb shell "su -c 'cp -f /data/local/tmp/build.prop.t1-7500-9000 /data/local/tmp/build.prop.trial-patched; sh /data/local/tmp/vendor-apply-trial.sh T1-7500-9000'"
adb reboot
```

On-device copies:
- `/data/local/tmp/build.prop.stock` (+ `/data/adb/sf_duration_rollback/build.prop.stock`) MD5 `fe6f8d95…`
- `/data/local/tmp/build.prop.t1-7500-9000` MD5 `681684cc…`
- `/data/local/tmp/build.prop.t2-6944-8500` MD5 `b5ef1471…`

Host:
- `D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\sf-duration-vendor-bake\vendor-offline-prep\`
- scripts: `vendor-apply-trial.sh`, `vendor-restore-stock.sh`, `vendor-verify-after-boot.sh`

## Honest follow-finger note

T2 moves work budget from **8.89 → 6.94 ms** (= one 144 Hz frame). That is the dumpsys target discussed for跟手.  
**Not claimed:** subjective跟手 win, black-screen immunity, or hardware success. User should真指验收; keep blackscreen ring ready.

## Related

- `LIVE-VENDOR-PROP-TRIAL.md` (donor-loose remount proof; superseded for “leave on device”)
- `DURATION-BOUNDS-20261106.md`
- `SF-DURATION-BOOT-HANG-NOT-ADOPTED.md` (Magisk closed)