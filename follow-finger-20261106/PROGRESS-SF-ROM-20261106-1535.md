# 收口 2026-11-06 15:35 Asia/Hong_Kong

hardware_success_claimed=false

## 交付路径
1. ROM bake-in 交接（无歧义）:
   - D:/TB371FC-release/clean-rebase-20261104/deploy-ready-20261106/display-refresh-system-v4/EXEC-FOR-CODEX.md
   - .../rom-stage/patch_my_product_tree.py
   - .../rom-stage/rebuild_my_product_erofs.sh
   - .../rom-stage/refresh_rate_config.xml (MD5 35db38f8…)
   - .../ROM-BAKE-IN-HANDOFF.md
   - 本机未产出 img（WSL CORRUPTED），未刷写；flash-candidate 仍 network-hold（整包勿刷）

2. SF 根因:
   - follow-finger-20261106/FLUENCY-SF-ROOTCAUSE.md
   - live 8.89/10.94 vs 144 周期 6.94；donor vendor 有 duration 段、实机无

3. SF Magisk trial:
   - deploy-ready-20261106/sf-duration-144-trial/ — **BOOT HANG NOT ADOPTED**，模块 disable
   - RESULT-BOOT-HANG-NOT-ADOPTED.md / VENDOR-BAKE-DRAFT.md

4. 保持 disable: dynframe、VRR TouchIdle-off、sf_duration_144
5. 保持 enable: tb371fc_system_refresh_policy（至 ROM bake 验收）
6. blackscreen ring: blackscreen-ring/ring-20261106-153325.log
