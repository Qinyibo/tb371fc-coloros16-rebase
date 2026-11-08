# FLASH-RESULT · Pen V4 on e088 · 2026-11-06

`hardware_success_claimed=false`

## Outcome

- **Flashed: YES** (5/5 forward sparse deltas Writing OKAY)
- Channel: bootloader fastboot (`is-userspace=no`)
- Script: `python tools/flash_candidate_delta.py --work pen-sharing-compat/candidate-v4-on-e088 --receipt .../physical-baseline-receipt.json`
- Reboot quirk: `fastboot reboot` returned `FAILED (Device sent unknown status code: u)` after all writes; device nonetheless left fastboot and reached `adb device` with `sys.boot_completed=1`
- userdata wipe: **no**
- Old V3→V4 deltas / V3 OFFLINE restore: **not used**

## Gate table (pre-flash, Asia/Hong_Kong)

| Gate | Expected | Measured | Result |
| --- | --- | --- | --- |
| Live physical super | e088d404d8e6e67f07820681f85259a62eee7911a0e5c24ef9c67b57aca03cdf | e088d404d8e6e67f07820681f85259a62eee7911a0e5c24ef9c67b57aca03cdf | PASS |
| boot_a | 5b4acefcc109ece2d3b84ce646b3496de6dfe2dc4b33d459bd2557d4d9a38b3a | 5b4acefcc109ece2d3b84ce646b3496de6dfe2dc4b33d459bd2557d4d9a38b3a | PASS |
| Refresh XML (pre) | MD5 35db38f8c85758c372546c707513642c | 35db38f8c85758c372546c707513642c | PASS |
| hwprofile super.sha256 updated to e088 | required before script | updated (+ system_a → e08a7e5c…) | PASS |
| Forward delta file SHAs | 1a5901ea… / 214704d4… / 73e7bfda… / c4a5f299… / 194535d6… | all matched | PASS |
| product | spinel | spinel | PASS |
| unlocked | yes | yes | PASS |
| current-slot | a | a | PASS |
| partition-size:super | 0x300000000 | 0x300000000 | PASS |
| battery-soc-ok | yes | yes (level 98) | PASS |
| is-userspace | no | no | PASS |
| Magisk refresh DISABLED; luna enabled; dynframe/vrr/sf DISABLED | required | matched | PASS |

## Before / after super

| | SHA-256 |
| --- | --- |
| BEFORE | `e088d404d8e6e67f07820681f85259a62eee7911a0e5c24ef9c67b57aca03cdf` |
| AFTER (readback) | `7b1c6736d45bf228a46df0e00dd2cd54e73cf1e36f6cf6a9bb08efbf2aba033d` |
| boot_a | unchanged `5b4acefcc109ece2d3b84ce646b3496de6dfe2dc4b33d459bd2557d4d9a38b3a` |

## Post-flash checks

| Item | Result |
| --- | --- |
| SELinux | Enforcing |
| Refresh XML MD5 | `35db38f8c85758c372546c707513642c` (preserved) |
| IPeManager.apk | `bfdae2e161774767a2c0dc94598fb78cdfa0e8063a00e7d6a459340311a956f2` |
| services.jar | `6a3caff3686b55ec58e492e8dc69090efe7c269e42327b454e0efe6308a8b490` |
| Magisk refresh module | still DISABLED |
| luna path B module | ENABLED; module lib SHA `2dc3bda37442e36f9fd6d3b2a19aec427e59c0393449f0ffb433095c94cf0b4e` |
| dynframe / vrr / sf_duration | still DISABLED |

## CoreService notes (vs V3 `app=null`)

- Package `com.oplus.ipemanager` present: versionName `16.13.0` / versionCode `16130000`, User0 enabled=default.
- Manifest registers `.btadsorb.CoreService`.
- Sample after unlock (~286s uptime): `dumpsys activity services com.oplus.ipemanager` → `(nothing)`; no IPeManager PID; boot logcat buffer had **0** lines matching IPeManager/btadsorb/CoreService start.
- Contrast V3 documented field case: system *did* initiate start but with `app=null` / empty PID.
- V4 this boot: **no automatic start attempt observed** in the sampled window. Not yet proven better or worse for real pen. Automatic start / manual start / real-pen checklist remain **PENDING**.

## Pen hardware checklist

| Item | Status |
| --- | --- |
| Connect / pair | PENDING |
| Battery | PENDING |
| Pressure | PENDING |
| Side button | PENDING |
| In-app writing | PENDING |
| Game / partial-app input | PENDING |

## Rollback (if needed while super is TO)

Use `pen-sharing-compat/candidate-v4-on-e088/rollback-v2/` reverse deltas → restores `e088d404…`. Do **not** restore V3 OFFLINE (would destroy refresh bake).

## Paths

- Work: `D:/TB371FC-release/clean-rebase-20261104/pen-sharing-compat/candidate-v4-on-e088/`
- Deploy doc: `D:/TB371FC-release/clean-rebase-20261104/deploy-ready-20261106/pen/DEPLOY-FROM-E088.md`
- This result: `D:/TB371FC-release/clean-rebase-20261104/deploy-ready-20261106/pen/FLASH-RESULT-E088-20261106.md`
- Fastboot log: `pen-sharing-compat/candidate-v4-on-e088/fastboot-20261106-171017.log`
- Receipt: `pen-sharing-compat/candidate-v4-on-e088/physical-delta-receipt.json`
- hwprofile backup: `candidate-hwprofile-current.json.bak-before-e088-20261106-170953`

## Blockers / open

- Real pen hardware acceptance not run → `hardware_success_claimed` stays **false**
- CoreService automatic start not observed yet; needs dedicated start/log + real-pen trial
- Script-level reboot assert failed (device recovered); next flash tooling may want tolerant reboot handling for this board

Written: 2026-11-06T17:16:50.327283+08:00 (Asia/Hong_Kong)
