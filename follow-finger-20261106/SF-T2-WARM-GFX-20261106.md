# SF-T2 warm-interrupt gfx — 2026-11-06

**Time:** 2026-11-06 18:37–18:39 Asia/Hong_Kong  
**hardware_success_claimed=false**  
**T2 rollback:** NOT done (left live)

## Pre-check (pass)

| Item | Live |
|------|------|
| `mWorkDuration` | **6.94** (`mReadyDuration=8.50`) |
| Refresh XML MD5 | `35db38f8c85758c372546c707513642c` (`/my_product/etc/refresh_rate_config.xml`) |
| PickRate | **144.00002**; Preferred/Default `[4,4,2,4]`; `mDefaultMaxRate=144.0` |
| Magisk SF modules | `tb371fc_sf_duration_144` **DISABLED**; `tb371fc_sf_duration_donor_loose` **DISABLED**; dynframe/VRR/refresh Magisk **DISABLED** |
| Luna Magisk | `tb371fc_luna_heap_offset_fix` ENABLED (path B; unrelated to SF) |
| T2 vendor props | `use_phase_offsets_as_durations=1`; app durations `6944444`; SF durations `8500000` (no high_fps phase props in `/vendor/build.prop`) |

## Protocol

- Script lineage: `_warm_switch_gfx.ps1` + swipe dwell from `warm-interrupt-trial.ps1`
- **NO force-stop / NO cold-start acceptance**
- Apps: WeChat / Douyin / Luna already open → 8× `am start -W` warm/hot switches + short swipe pair per cycle
- Dump dir: `follow-finger-20261106\warm-switch-gfx-T2-20261106-183750\`
- LaunchState mixed WARM/HOT after pool warm; Luna first open logged COLD once then HOT (expected if not previously resident)
- Live PIDs after run (distinct, still alive): mm=`9305` aweme=`16863` luna=`16724`
- Limitation: **no true finger** — adb swipe + gfxinfo only; subjective fluency still needs user

## T2 numbers (this run)

| App | frames | janky% | High input latency | p50 | p90 | p95 | Missed Vsync | deadline missed |
|-----|--------|--------|--------------------|-----|-----|-----|--------------|-----------------|
| WeChat | 528 | **27.84%** | 689 | 14ms | **31ms** | 48ms | 34 | 147 |
| Douyin | 211 | **38.86%** | **225** | 16ms | **65ms** | 113ms | 37 | 82 |
| Luna | 452 | **29.65%** | 621 | 11ms | **44ms** | 133ms | 52 | 134 |

PickRate stayed **144** across smsum cycles (`current mode` fps=144).

## vs prior (stock / 8.89-era warm-switch)

Primary same-protocol baseline: `warm-switch-gfx-20261106-144225`  
Label: `A_BASELINE_before_sf_duration_trial` (documented in `FLUENCY-144-NEXT.md` as Fresh warm metrics 14:42) — SF then still **8.89** class.

| App | metric | Baseline 144225 (8.89 era) | T2 now (6.94) | delta |
|-----|--------|----------------------------|---------------|-------|
| WeChat | janky% | 16.74 | 27.84 | **worse** |
| WeChat | p90 | 23ms | 31ms | **worse** |
| WeChat | High input | 669 | 689 | ≈ flat |
| Douyin | janky% | 29.26 | 38.86 | **worse** |
| Douyin | p90 | 46ms | 65ms | **worse** |
| Douyin | High input | 379 | 225 | **better** |
| Luna | janky% | 32.60 | 29.65 | slight better |
| Luna | p90 | 38ms | 44ms | slight worse |
| Luna | High input | 504 | 621 | **worse** |

Secondary (different protocol / earlier unlocked focus dumps `multi-gfx-20261106-132837`): WeChat High input **155**, Luna **1082**, Douyin n/a in that table’s douyin slot — **not same warm-switch protocol**; do not treat as ABA peer. Note that dump also showed SF active mode often **120** while PickRate claimed 144 (pre-bake era).

## Verdict

- **gfx vs 8.89 warm baseline: inconclusive → lean slightly worse** on janky%/p90 for WeChat & Douyin; Douyin High input improved alone; Luna mixed.
- **Does NOT prove subjective follow-finger win.** User true-finger warm interrupt remains the gate.
- **Device still on T2:** `mWorkDuration=6.94`, PickRate 144, refresh MD5 `35db38f8…`, SF Magisk duration modules disabled. **No T2 rollback.**

## Blackscreen ring

- Restarted 18:37 Asia/Hong_Kong: `D:\TB371FC-release\clean-rebase-20261104\blackscreen-ring\ring-20261106-183738.log`
- Confirmed growing (~19.4 MiB by 18:39); `CURRENT.txt` points at this file.

## Next (if user okays)

1. User true-finger warm interrupt among WeChat/Douyin/Luna — accept/reject T2 on feel  
2. If feel worse: keep dumps, consider T2 rollback path (restore prior `/vendor/build.prop` duration block) — **not done this turn**  
3. If feel better despite gfx: keep T2, re-run warm gfx after longer soak / thermal settle