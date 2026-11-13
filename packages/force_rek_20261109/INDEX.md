# Force REK diagnostic · 2026-11-09

`hardware_success_claimed=false`

休眠黑屏这条的内核路径有记录：`r108-force-rek` #45，`0xA0` → host `0x23 0x00` → `0xA1` / `FORCE_REK_STATE_OK`，`mScreenState=ON`。DIMNESS-DIAG 记最大亮度仍略暗、画面可见，不把略暗写成黑屏失败。不是键盘硬件成功，也不是整机验收。

## Included

- `scripts/apply_force_rek.py`：往 r108 树的 `nvt_panel_resume_commit` 插入 Force REK 诊断（不伪造 A3，失败不打开 IRQ）
- `scripts/build_force_rek.sh` / `pack_force_rek.sh` / `pack_force_rek.ps1` / `force_rek_soak.ps1`
- `force-rek/resume_pack_flash.sh` / `STATUS.md` / `DIMNESS-DIAG-20261109.md`
- 包根 `BOOT-DIAG-20261109.md` / `BOOT-FIX-20261109.md` / `BOOT-FIX-ROOTCAUSE-20261109.md`（救砖与开机门槛；同一份也在 `field-notes-20261109/`）
- `boot-diag/panel-force-rek-20261109-202747-SUMMARY.txt` 与 meta / backlight / dmesg-panel 摘录

## DO NOT

- 不要只加 Tinno device manifest、不改 matrix 的 `vendor.mediatek…` 名（HAL 是 `vendor.qti…`）。半套会砖。见 `field-notes-20261109/vintf-DO-NOT-APPLY/`。
- 不要 remount `/vendor` rw，不要关 verity / 改 vbmeta 来“修”启动。
- 不要 userspace 拉住 `mcu_resume` GPIO。

## Excluded（local-only / Release 候选，不入库）

boot 不在本仓库，留在 Qin `E:\youxikaifa\work\today-20261109\`（`force-rek/STATUS.md`）：

| 文件 | SHA256 |
| --- | --- |
| `boot-diag/boot-r108-force-rek-magisk.img`（刷入 `boot_a` 的那份） | `71340E8D8751C9951844C4BDBEFB1BDB49F75EE8F41F06F4B33811B9A9F5AA3E` |
| `boot-r108-force-rek.img` | `54471AF4DDCEC36E98BE28C4A73C7B88E637A6D5395564A189AD7A4EADCA4994` |
| Image | `2CB1B19D7D7C3480E59AA3B255F8A8686A923ACB5CE9B1750D82FF7625AD6D80` |

未收录 panel dumpsys `display.txt` / `power.txt`（数万字节 dumpsys）。未收录 super / vendor 镜像。打包脚本会调用本机 `magiskboot`，该二进制不在 git。
