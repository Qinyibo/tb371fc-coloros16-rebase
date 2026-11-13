# Field notes · TB371FC ColorOS 16 · 2026-11-09/10

`hardware_success_claimed=false`

来源：Qin `E:\youxikaifa\work\today-20261109` 的 lean pack（见 `PACK-MANIFEST.md`）。键盘硬件未成功。

`README.md` 是 2026-11-09 01:30 的早期记录（当时键盘仍未修）。当晚及 11-10 的笔记在后：Magisk 成对 VINTF 已装且 HAL 在跑，物理 POGO 仍是 `present=0`。早期 README 里「不要只加 manifest 片段」仍然有效；「键盘未修、明天再弄」被后面的软件 PASS + 物理 FAIL 取代，不能把 01:30 当成最终状态。

## Included

- `BOOT-DIAG-20261109.md` / `BOOT-FIX-20261109.md` / `BOOT-FIX-ROOTCAUSE-20261109.md`
- `boot-diag/`：kb attach / reseat 小状态、`pogo-power` / `pogo-tablet-side`、`online-present-root` 与其引用的 `_online_present_*.txt`、`kb-batt-bypass`、`touch-runaway`、Force REK SUMMARY/meta/backlight
- `boot-diag/compatibility_matrix.dev.xml`：库存矩阵名是 `vendor.mediatek.hardware.tinno_keyboard`
- `display_brightness_config_default.orig.xml` 与 `_x2.xml`
- `bili-fullscreen/`：B 站 magicwindow 脚本
- `vintf-DO-NOT-APPLY/`：半套片段警告样本，不是修复
- `qin-pc/`：Qin 电脑 C: / D: 笔记，不是平板刷机事实

成对模块与 Force REK 脚本在 `packages/tinno_vintf_pair_20261109/`、`packages/force_rek_20261109/`。

## 记录里已经写明的边界

- 物理 POGO `present=0` / `online=0`。MCU `online`（HID `inbuf[3]` bit0）会短暂置位再掉。`kb_batt_level`（`inbuf[9]`）是遥测，不是连接门。用户说明键盘包不可充电，不要建议给键盘充电。
- 触控乱跑：NVT 电容鬼触，键盘靠近玻璃时加重；不是 Lenovo HID 洪水。
- 不要 GPIO / `mcu_resume` 拉高（有 bootloop 记录）。
- 不要关 verity / 改 vbmeta。

## Excluded

- `boot-r108-force-rek*.img`、`boot-r108-resx-magisk*.img` 及 super/vendor 镜像（Qin E:，local-only / Release 候选）
- Magisk 工具脚本 `magisk30.7-tools/`（含默认可能关掉 verity 的 `boot_patch.sh`）
- `boot-diag/` 里一次性探针脚本（含 GPIO hold/pulse）。结论已写在上述 markdown，不把那些脚本当成可再跑的修复
- dumpsys 大段：`panel-force-rek-*-display.txt`、`*-power.txt`；`kb-vintf-live/` 整份 vendor manifest；`vendor_manifest.dev.xml`；空文件
- `pogo-power` 原文有两处 NUL，入库文本已删掉这 2 字节，其余措辞未改
- `kb-reseat-20261109-221838.txt` 原文是 UTF-16 LE，入库改为 UTF-8，措辞未改

`hardware_success_claimed=false`
