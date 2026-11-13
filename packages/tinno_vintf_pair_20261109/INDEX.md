# Magisk systemless paired Tinno VINTF · 2026-11-09

`hardware_success_claimed=false`

软件侧：模块已装，`init.svc.tinnokeyboard=running`，lshal 有 `vendor.qti.hardware.tinno_keyboard@1.0::ITinnoKeyBoard/default`。这不是键盘硬件成功。物理 POGO 仍是 `present=0`。

## DO NOT — 半套 VINTF

不要只写入 device manifest 片段。库存 `compatibility_matrix.xml` 写的是 `vendor.mediatek.hardware.tinno_keyboard`，HAL / 片段是 `vendor.qti.hardware.tinno_keyboard`。只加片段会 VINTF 校验失败并 bootloop。

不要 `mount -o remount,rw /vendor`。remount 写入打坏 dm-verity，删掉片段也不能恢复。失败样本在 `field-notes-20261109/vintf-DO-NOT-APPLY/`（警告，不是修复）。

不要把关 verity / 改 vbmeta 当成修复。本包文档要求 `KEEPVERITY=true`、`PATCHVBMETAFLAG=false`。

## Included

- `module/`：systemless 模块树（`system/vendor/etc/vintf/` 下成对的 matrix + manifest 片段）
- `tb371fc_tinno_vintf_pair.zip`：同上内容，SHA256 `16E3F4FF045D824482EFCD5CE92251129A8FCB2326F38BC36978AD6CF3AB2078`
- `README.md` / `STATUS.md` / `flash-install.sh` / `flash-install.ps1`
- `install-verify-20261109-214451.txt`：Force REK Magisk boot 上重装模块后的核对（未再刷 tinno overlay boot）

## Excluded（local-only / Release 候选，不入库）

镜像留在 Qin `E:\youxikaifa\work\today-20261109\kb-vintf-magisk\`，约 96MB 级 boot，不提交：

| 文件 | SHA256 | 记录 |
| --- | --- | --- |
| `boot-r108-resx-magisk.img` | `62428F25F857BCC15FE8AB4A3A18148C5B37723109DE60F974C470188839A825` | 纯 Magisk 30.7 |
| `boot-r108-resx-magisk-tinno.img` | `1C573C2E6B83C212A217884F771A9AE722D3956B51B8F2075C10499D1E86C2DB` | STATUS 记当晚刷过；21:44 核对改为保留 Force REK Magisk boot |
| `boot-r108-resx.img` | `F5F446047721E788451FBDE8D984A8E3DCA0AC21E18E85F9F15839C6289B1F13` | stock rollback |

未收录 `magisk30.7-tools/boot_patch.sh` 与 `util_functions.sh`。那是 Magisk 工具脚本，不是本模块源码；`boot_patch.sh` 在未设置时默认 `KEEPVERITY=false`，不能当成关 verity 的修复说明。
