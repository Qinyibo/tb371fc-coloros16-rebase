# Pen V4 GATE ABORT · 2026-11-06

`hardware_success_claimed=false`

**Decision: ABORT. No flash performed.**

Physical super SHA-256 no longer equals V3 baseline. Forward V3→V4 delta (`tools/flash_candidate_delta.py --work pen-sharing-compat/candidate-v4 ...`) is unsafe on this device state. Do not apply reverse V4→V3 deltas either (device is not on V4).

## Gate table

| Gate | Expected | Measured | Result |
| --- | --- | --- | --- |
| Work root materials | `tools/flash_candidate_delta.py`, `candidate-v3`, `candidate-v4`, V3 OFFLINE rescue | Present under `D:/TB371FC-release/clean-rebase-20261104` | PASS |
| V4 forward delta file hashes (5 parts) | DEPLOY / `delta-result.json` SHA-256 list | All 5 match on disk | PASS |
| `boot_a` physical SHA-256 | `5b4acefcc109ece2d3b84ce646b3496de6dfe2dc4b33d459bd2557d4d9a38b3a` | `5b4acefcc109ece2d3b84ce646b3496de6dfe2dc4b33d459bd2557d4d9a38b3a` via Magisk `sha256sum /dev/block/by-name/boot_a` | PASS |
| Physical `super` SHA-256 | V3 `cac703a493dce9be832c3ca81a01b4ca74c47852bc0ad2ff7ac275cb314e5a9e` | **`e088d404d8e6e67f07820681f85259a62eee7911a0e5c24ef9c67b57aca03cdf`** via Magisk `sha256sum /dev/block/by-name/super` | **FAIL** |
| Target would be V4 | `31dbe4eafed965806ff4de4242f44103056ada235bdc0dea7acaaaea2470908e` | Current ≠ V3 and ≠ V4 | N/A (precondition broken) |
| Bootloader getvar `product=spinel`, `unlocked=yes`, `current-slot=a`, `partition-size:super=0x300000000`, `battery-soc-ok=yes`, `is-userspace=no` | All match | **Not measured** — aborted before `adb reboot bootloader` because super gate already failed. Android-side: `ro.product.board=spinel`, slot `_a`, battery level 98 USB-powered, serial `HA1W0JA3`, build `OPD2413_16.0.10.600(CN01)`, SELinux Enforcing, Magisk 31.1 | SKIPPED |
| Host `candidate-hwprofile-current.json` | Should reflect live device | Still records boot=`5b4ace…` and super=`cac703a…` (stale vs live super) | STALE / misleading |
| `deploy-ready-20261106/pen/rollback.json` | Present per DEPLOY authority list | **Missing** (copies exist at `handoff-to-grok-20261106/pen/rollback.json` and `pen-sharing-compat/candidate-v4/rollback-v2/rollback.json`) | NOTE (not the abort cause) |

## Why super diverged

Today’s refresh live-bake wrote into the live `system` tree under `/my_product` (logical `system_a` → `dm-2`). Evidence:

- `/my_product/etc/refresh_rate_config.xml` mtime **2026-11-06 16:30:37 +0800** (Asia/Hong_Kong), size 198373
- That remount write mutates `system_a` contents inside physical `super`, so the partition is no longer bit-identical to V3 `cac703a…`
- Measured live super `e088d404…` is neither V3 nor V4

Therefore the V4 sparse deltas (built against V3 base bytes at `system_a` start_sector 79872, changed_raw_bytes 114536448) must not be flashed: they assume exact V3 baseline bytes in the patched spans.

## Materials checked (not invented)

- `D:/TB371FC-release/clean-rebase-20261104/deploy-ready-20261106/pen/DEPLOY.md`
- `D:/TB371FC-release/clean-rebase-20261104/tools/flash_candidate_delta.py`
- `D:/TB371FC-release/clean-rebase-20261104/pen-sharing-compat/candidate-v3/` (incl. `physical-delta-receipt.json`, `physical-super-sha256.txt`)
- `D:/TB371FC-release/clean-rebase-20261104/pen-sharing-compat/candidate-v4/` (5 forward deltas + `delta-result.json` + `rollback-v2/`)
- Rescue: `pen-sharing-compat/super-pen-sharing-v3-OFFLINE.img` (12884901888 bytes) and V4 OFFLINE sibling present
- Handoff inventory: `handoff-to-grok-20261106/pen/image-inventory.json`, `execution-environment.md`, `rollback.json`

## Flash script caveat

`flash_candidate_delta.py` live-checks only `boot_a` on device; super baseline is asserted against host `candidate-hwprofile-current.json` + receipt, **not** a fresh physical `sha256sum` of `/dev/block/by-name/super`. DEPLOY’s “重读当前物理 super” gate caught the mismatch the script alone would miss. Do not bypass by editing the host JSON.

## Required recovery before any pen V4 flash

Pick one explicit restore path (operator choice; not executed in this abort):

1. **Preferred for pen track:** restore full physical super from `pen-sharing-compat/super-pen-sharing-v3-OFFLINE.img` via bootloader fastboot (product=spinel channel), then re-hash to confirm `cac703a…`, then run the official V3→V4 delta flash.
2. Or rebuild a new pen candidate whose `base_super_sha256` equals the **current** live super `e088d404…` (and re-derive deltas) — out of scope for this DEPLOY path.

Do **not**:

- Flash V4 deltas onto `e088d404…`
- Flash unrelated `super-cleanbase*` images for this pen step
- Add `--allow-vendor-*` flags
- Claim hardware success without a physical pen checklist

## Hardware checklist

All physical-pen items remain **PENDING / cannot complete** (no flash, no pen):

- connect / battery / pressure / side button / in-app writing vs game input

`hardware_success_claimed=false`

## Outcome

- Flashed: **no**
- Super before (live): `e088d404d8e6e67f07820681f85259a62eee7911a0e5c24ef9c67b57aca03cdf`
- Super after: unchanged (no write)
- boot_a: unchanged `5b4acefcc109ece2d3b84ce646b3496de6dfe2dc4b33d459bd2557d4d9a38b3a`
- CoreService / post-flash logs: not applicable
- Blocker: physical super ≠ V3 after today’s `/my_product` refresh bake
- Doc: this file
