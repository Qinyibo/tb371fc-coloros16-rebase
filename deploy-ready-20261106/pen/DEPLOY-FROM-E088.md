# Pen V4 · FROM live e088 (post refresh bake) · DEPLOY

`hardware_success_claimed=false`
**Flash in this rebuild task: NOT done.** Offline package verified.

## OBSOLETE note

`deploy-ready-20261106/pen/DEPLOY.md` (V3 `cac703a…` → V4 `31dbe4ea…`) and its five old forward deltas are **OBSOLETE** after the 2026-11-06 refresh XML live-bake mutated physical super to `e088d404…`.
Do **not** use old `candidate-v4/super-delta-0*.img`. Do **not** restore `super-pen-sharing-v3-OFFLINE.img` (would destroy refresh bake PASS).

See also: `GATE-ABORT-20261106.md` (why old path aborted) and `GATE-E088-20261106.md` (this path).

## Identity gates (must all pass before flash)

| Item | Expected |
| --- | --- |
| Work root | `D:/TB371FC-release/clean-rebase-20261104` |
| Channel | Bootloader **fastboot** (`is-userspace=no`) |
| Device | `product=spinel`, `unlocked=yes`, slot `a`, `partition-size:super=0x300000000`, `battery-soc-ok=yes` |
| Current physical super | `e088d404d8e6e67f07820681f85259a62eee7911a0e5c24ef9c67b57aca03cdf` |
| boot_a | `5b4acefcc109ece2d3b84ce646b3496de6dfe2dc4b33d459bd2557d4d9a38b3a` (unchanged) |
| Target super | `7b1c6736d45bf228a46df0e00dd2cd54e73cf1e36f6cf6a9bb08efbf2aba033d` |
| Delta scope | only `system_a`, RAW changed `114536448` |
| Refresh XML after flash | `/my_product/etc/refresh_rate_config.xml` MD5 `35db38f8c85758c372546c707513642c` (verified inside TO image offline) |
| Magisk | refresh DISABLED; luna path B enabled; dynframe/vrr/sf_duration DISABLED |

**Also re-hash physical `/dev/block/by-name/super` on device immediately before flash** (script alone trusts host `candidate-hwprofile-current.json`).

## Approach used

1. adb dump live `system_a` → `system-live-e088.img` (sha256 `e08a7e5c…`)
2. Copy V3 OFFLINE super + splice live system_a @ start_sector 79872 → reconstructed `super-live-e088.img` verified `e088d404d8e6e67f07820681f85259a62eee7911a0e5c24ef9c67b57aca03cdf`
3. Copy live system → mount ext4 → replace only IPeManager.apk + services.jar with pen V4; refresh XML untouched (MD5 `35db38f8…`)
4. `tools/build_candidate_delta.py` → forward sparse deltas + complete TO super
5. `tools/build_reverse_delta.py` → `rollback-v2/`

## Forward flash (e088 → pen-V4-on-e088)

Prep host JSON first (required by `flash_candidate_delta.py`):

- Set `candidate-hwprofile-current.json` `super.sha256` = `e088d404d8e6e67f07820681f85259a62eee7911a0e5c24ef9c67b57aca03cdf` (and logical `system_a` = `e08a7e5c…`)
- Receipt: `pen-sharing-compat/candidate-v4-on-e088/physical-baseline-receipt.json`

```
python tools/flash_candidate_delta.py --work pen-sharing-compat/candidate-v4-on-e088 --receipt pen-sharing-compat/candidate-v4-on-e088/physical-baseline-receipt.json
```

Forward delta SHA-256:

1. `1a5901ea804ee0c3f3bc85e193d30a49309c4b3dcae978a57724db5891a3bc49`
2. `214704d49df0253c6c9a20d89ea9d8a396e72fdac14b492e4a49b082450226a6`
3. `73e7bfdabc7169b25fea51a8bfd0f79c204cca1ab18888e760a2c3df56366d93`
4. `c4a5f29944d4174dffae1dc3076b47b2d6c0b95fd4710441ac343b7121fb1d80`
5. `194535d6379e90ab444653f471fc7f3f86333e321bd8f65f6f7635a99d74f732`

## Rollback (only if current super is already TO `7b1c6736…`)

Use `pen-sharing-compat/candidate-v4-on-e088/rollback-v2/`:

1. `50b452b13099eed6a877270434163feb0afde55bbaeb5d6c64bbd1a8268421b4`
2. `9e6167bd44d83e47c225dc483de704185b175772fcdd9ae4b5e9d520fa5a43a7`
3. `f6c3f7907d102863f8344bf231aab5fb7c23864d43bd9e6616ac8aa2b7c0230a`
4. `5d90d74d319355717f63e968dba32522560f0711b9a97034dfc79556411578f1`
5. `59ae35c29b123fc5f57150defdfb116223c8a88fd90b5c2aeee0e5533b9db679`

Restores super `e088d404d8e6e67f07820681f85259a62eee7911a0e5c24ef9c67b57aca03cdf`. `userdata_wipe_required=false`.
If partial flash / mismatch: **do not** restore V3 OFFLINE; use TO/e088 complete images instead.

## Post-flash checklist (any fail ⇒ keep hardware_success_claimed=false)

1. Enforcing; super readback = `7b1c6736…`; boot unchanged; refresh XML MD5 still `35db38f8…`
2. CoreService vs V3 `app=null` behavior
3. Real pen: connect / battery / pressure / side button separately
4. In-app writing vs game input separately
5. Magisk module states unchanged as required

## Paths

- Work: `pen-sharing-compat/candidate-v4-on-e088/`
- Deploy mirror: `deploy-ready-20261106/pen/delta-from-e088/`
- This doc: `deploy-ready-20261106/pen/DEPLOY-FROM-E088.md`
