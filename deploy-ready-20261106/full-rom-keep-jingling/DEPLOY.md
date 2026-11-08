# DEPLOY · KEEP + 鲸鲮 Office V2.1 完整刷机包

`hardware_success_claimed=false`

## 包路径（二选一，内容相同）

1. `D:\TB371FC-release\ColorOS16_TB371FC_KEEP_jingling_20261107_CANDIDATE\`  ← 对外完整刷机包（v27 同款结构）
2. `D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\full-rom-keep-jingling\`
3. 工作镜像：`D:\TB371FC-release\clean-rebase-20261104\pen-sharing-compat\candidate-keep-jingling-20261106\`

## 镜像

| 分区 | 文件 | SHA-256 |
|------|------|---------|
| super | images/super-KEEP-jingling.img | `9845539c7c139cc08408bbc6f9a3d9c1653c0b84821e6170993f651df73c27cb` |
| boot | images/boot_a.img | `5b4acefcc109ece2d3b84ce646b3496de6dfe2dc4b33d459bd2557d4d9a38b3a` |
| vbmeta | images/vbmeta_a.img | `5faf802f3d821512505c42a9fa0dba5b969f135fd5ec3bf6686e8448e741a169` |
| vbmeta_system | images/vbmeta_system_a.img | `848f04a7cf01cbfc68640ece4895e1aa00c6ba5cbf385c81b395f51da0829fef` |

FROM KEEP super：`7b1c6736…`（pen-v4-on-e088）。鲸鲮烤入 `/system/app/YozoOffice/YozoOffice.apk`（SHA `0cc7977d…`）。腾空间删除 `my_product/del-app/WpsLauncher`。refresh XML 仍为 `35db38f8…`。`wipe_userdata=false`。

## 执行顺序

1. `1-连接检查.cmd`
2. `2-刷前检查.cmd`
3. 已在 KEEP 上：优先 `一键刷入-delta.cmd`；否则 `一键刷入-完整super.cmd`
4. `核验ROM.cmd`（刷后禁用 Magisk jingling 模块，确认 APK 来自真实 system）

## ASCII 刷入入口（2026-11-07 编码修复）

请双击 **FLASH.cmd**（推荐 delta）。另有 check1.cmd / check2.cmd / flash-delta.cmd / flash-full.cmd / verify.cmd。
中文名 cmd 仅为兼容，内部已改为 call ASCII 入口，避免 UTF-8 vs GBK 乱码。
