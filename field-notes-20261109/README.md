# 2026-11-09 今日操作记录与恢复包

## 当前状态（2026-11-09 01:30，最终）

- 设备：TB371FC（spinel），已恢复到 **ColorOS 16 端口 v27（OPD2413_16.0.0.210(CN01)）**，数据已清空。
- 刷入方式：`R94T-v27-r106-20261103-CANDIDATE` 的 **32MB 预分块 + 断点续传** 脚本（super 385 块、boot、vbmeta；用户原有刷法）。
- 启动：已刷 **r108 boot**（`boot-r108-pen.img`，SHA256 35bab398…），内核 `#45`。
- 亮度：×2 表通过 Magisk 模块 `tb371fc_brightness_x2` 的 `post-fs-data.sh` bind mount 持久化，`/system_ext/etc/display_brightness_config_default.xml` 哈希 `823397de…`。
- B 站：`/my_product/etc/fantasy/sys_fantasy_window_managed.xml` 已移除 `tv.danmaku.bili` magicwindow 条目（version 20253026）；运行期 `fantasywindow.db` 已删除并由系统重建，当前无 B 站 magicwindow 行 → B 站全屏运行。
- 键盘（磁吸）：**未修复**，按用户要求明天再弄。Tinno HAL 的 VINTF manifest 问题仍在；**不要**只加 `vendor.qti.hardware.tinno_keyboard` 的 device manifest 片段（会 bootloop），正确做法是同时处理 `/vendor/etc/vintf/compatibility_matrix.xml` 的 `vendor.mediatek...` 名称不一致。
- 设备已关机。

## 之前尝试的记录（已废弃）

- 曾刷 `clean-flash-staging-20261107`（金标/clean ROM），385 块全部写入但设备卡联想 logo 重启，未启动；之后用 R94T-v27-r106 端口包恢复。
- 曾尝试 VINTF 键盘片段导致 bootloop；已回滚。


## 今天做过的操作（按时间）

### 1. B 站全屏（ColorOS 端口）
- 原因：ColorOS 的 magicwindow 双窗把视频详情页放右 pane，播放器手势区域与窗口不一致。
- 操作：
  - 从 `/my_product/etc/fantasy/sys_fantasy_window_managed.xml` 删除 `tv.danmaku.bili` 的 magicwindow 条目（version 20253028）。
  - 从运行期库 `/data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db` 的 `t_config` 删除 `tv.danmaku.bili / magicwindow` 行（实际生效来源）。
- 结果：B 站任务变为 `mode=fullscreen`。
- 备份：`fantasywindow.db.bak`、设备 `/data/adb/tb371fc-capture/backup/sys_fantasy_window_managed.xml.pre_bili_disable`。

### 2. 亮度 ×2（ColorOS 端口）
- `/system_ext/etc/display_brightness_config_default.xml` 改为 ×2 表（8191→4094）。
- 原备份：`display_brightness_config_default.orig.xml`；模块回退：`tb371fc_brightness_x2.zip`。

### 3. r108 RESX（ColorOS 端口内核）
- 修复黑屏后触控 REK 卡 0xA0：`nvt_resume_release_from_reset()`。
- boot：`boot-r108-resx.img`（SHA256 f5f44604…），pen 版 `35bab398…`。
- **注意：这是 ColorOS 端口内核，不要刷到金标/clean ROM 上。**

### 4. oplus-services.jar 启动窗口补丁（已回滚）
- v1 条件过宽，破坏了堆叠后台；已恢复原版 jar（a5928b09…）。
- v2b 未安装。clean ROM 不需要。

### 5. VINTF 键盘修复（失败，勿再应用）
- 问题：Tinno 键盘 HAL `vendor.qti.hardware.tinno_keyboard@1.0::ITinnoKeyBoard/default` 不在 device VINTF manifest。
- 添加 `/vendor/etc/vintf/manifest/vendor.qti.hardware.tinno_keyboard@1.0-service.xml` 后 bootloop。
- 原因：device manifest 与 `/vendor/etc/vintf/compatibility_matrix.xml` 里的 `vendor.mediatek...` 名字不一致，VINTF 校验失败。
- 已从 TWRP 删除该片段，但设备仍 bootloop，最终整包清刷。
- **不要再次直接加该片段。**

## clean ROM 刷完后的检查清单

1. 开机：`ro.build.display.id`、`ro.product.model` 确认是金标/clean ROM。
2. B 站：金标自带双窗/适配；先不要套用 ColorOS 的“删 magicwindow”修复，确认手势是否正常。
3. 磁吸键盘：金标 vendor 应带正确的 Tinno VINTF 条目，先测试；若仍无效，再按安全方式排查（不要直接加片段）。
4. 亮度：金标通常原生亮度，不需要 ×2 表；如偏暗再评估。
5. 黑屏：金标内核与 ColorOS 端口不同；先观察，若复现再针对该内核做 r108 类修复。
6. 如果以后回到 ColorOS 端口：再按本记录重做 B 站全屏、亮度 ×2、r108 boot；VINTF 片段仍不要加。

## 文件

- `boot-r108-resx.img`：ColorOS 端口 r108 内核（勿用于金标）。
- `display_brightness_config_default_x2.xml` / `.orig.xml`：亮度表。
- `bili-fullscreen/`：B 站全屏脚本与 DB 备份。
- `vintf-DO-NOT-APPLY/`：失败片段与说明。
- `vendor-restore/`：vendor 镜像路径与 dd 脚本（ColorOS 端口 v24 vendor）。
- `scripts/`：今日诊断/恢复脚本。
