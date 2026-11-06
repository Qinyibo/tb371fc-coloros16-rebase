# V4 执行环境与回退边界

工作根 `D:/TB371FC-release/clean-rebase-20261104`，PowerShell 先加载 `task_env.ps1`，TEMP/TMP 和 Java 临时目录在 D 盘。镜像集成在 `TB371FC-Builder` 的 `/mnt/d/TB371FC-release/clean-rebase-20261104`，使用 `pen-sharing-compat/integrate-pen-v4.sh`。离线修改限定在 `system_a` 中的 IPeManager 和 services.jar。

实际写入通道是 **Bootloader fastboot**，校验 `is-userspace=no`、`product=spinel`、`unlocked=yes`、slot `a`、super 大小 `0x300000000`。现有刷写器以 `--work pen-sharing-compat/candidate-v4 --receipt pen-sharing-compat/candidate-v3/physical-delta-receipt.json` 为 V3 → V4 调用参数。这里仅登记参数，未执行。开刷前需重新读回并确认当前物理 super 与 V3 基线一致，同时核对 boot。工具对差分块验证目标边界与完整候选字节。

现行流程依赖现装的 Magisk 31.1 提供 root 读回校验。V4 的笔代码本身不依赖 Magisk 模块，刷写保留 boot_a 原样，预期 SHA-256 `5b4acefcc109ece2d3b84ce646b3496de6dfe2dc4b33d459bd2557d4d9a38b3a`。回退使用 `pen/rollback.json` 对应的五段反向差分。它以完整 V4 super 为适用前提。部分刷入、基线不符或无法验证分区状态时，不可把 V4→V3 反向差分当通用救援，保留完整 V3 镜像。

D 盘权威记录：

- `D:/TB371FC-release/clean-rebase-20261104/pen-sharing-compat/build-v4/pen-build-result.json`
- `D:/TB371FC-release/clean-rebase-20261104/pen-sharing-compat/pen-v4-integration.json`
- `D:/TB371FC-release/clean-rebase-20261104/pen-sharing-compat/build-v4/container-checks.json`，本目录副本名为 `offline-container-checks.json`。
- V3 原始服务现场 `D:/TB371FC-release/clean-rebase-20261104/pen-sharing-compat/candidate-v3/first-boot-state.txt`。

V4 未刷入，实际开机、真笔、充电配对和游戏／部分应用输入仍待验证。任何可部署草案都应把这些与构建成功分开。
