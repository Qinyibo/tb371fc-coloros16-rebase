# Codex 可部署交接 · 2026-11-06（tip handoff `55b8fe6`）

`hardware_success_claimed=false`。本包只交离线可执行草案；真机结果由 Codex 验收后另写。

输入材料：仓库 `handoff-to-grok-20261106/` + D 盘原件路径见 INDEX。主机写入只限 D 盘。不碰 ART／GC／全局厂商标识／频率／白名单叠层。

优先级执行顺序：

1. **汽水有限处理（可部署）** → `music/DEPLOY.md`
2. **笔 V4（可部署刷入／回退，未做真笔验收）** → `pen/DEPLOY.md`
3. **通信共享（仅试跑清单）** → `comm/TRIAL.md`
4. **竖屏多任务／流畅度（仅观察／试跑）** → `recents-scheduler/TRIAL.md`

总验收门禁见文末。

## 总门禁

- 汽水：完成 `music/DEPLOY.md` T1 且未触否定条件 → 可记“有限处理已部署待长期观察”；仍非 hardware_success。
- 笔：完成刷入哈希门禁 + 分项验收；任一项硬件未测 → 不得宣称笔通过。
- 通信／多任务／流畅度：只交试跑；无真机结果不得写通过。
- 全程：`hardware_success_claimed=false`，直至分项证据满足且用户／Codex 显式改写。

## 本包文件

见同目录 `SHA256SUMS.txt`。请把整个 `deploy-ready-20261106` 放到  
`D:/TB371FC-release/clean-rebase-20261104/deploy-ready-20261106/`。
