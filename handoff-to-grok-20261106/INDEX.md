# TB371FC 离线交接 · 2026-11-06

母包 `OPD2413_16.0.10.600(CN01)`。实装基线为笔／通信 V3，V4 已构建、待实机。优先级为汽水有限处理 → 笔／通信 → 竖屏多任务 → 流畅度。此目录只交接已有材料，刷写、设备配置和运行参数留待另行执行。主机写入限 D 盘。

已有的脱敏墓碑、位图和 provider 反汇编、逐帧 CSV／SQL 与实验条件见 [tip dcd5b42 的证据索引](../evidence/2026-11-06/README.md)。目录中的二进制按原字节保存。`music/music-installed.apk` 使用 Git LFS，Git 浏览器或 API 可能只展示指针。用具有该私有仓库权限的 `git lfs pull` 可取原件，再核对 SHA-256。

| 项 | 状态与路径 |
| --- | --- |
| 1. libsysoptimizer | **已放** [原件](music/libsysoptimizer.so)。arm64，Build ID `5ba6754a5e6f6684715e45f17c582f47de746879`，SHA-256 `e8357c10cef28edb36ad59faeec51d120c9ae41f04ff3de8f5874349dc5f7ec3`。与 APK 内 `lib/arm64-v8a/libsysoptimizer.so` 字节一致。原始路径见身份记录。 |
| 2. libart | **已核对本地原件**，设备路径 `/apex/com.android.art/lib64/libart.so`，D 盘副本 `D:/TB371FC-release/clean-rebase-20261104/scheduler-compat/gpu-floor-native-v7/sameboot-aba/libart.so`，SHA-256 `63ed6aa8ffbc82db163faaaf5bd1cf0e3bdf1138af7e0d32bab80283e6e2452a`，Build ID `6116d0e56573559ea90cc3bf6e88c9f7`。依据既有实读及本次副本校验。 |
| 3. 汽水安装包 | **已放** [原件](music/music-installed.apk)，Git LFS。保存的安装 APK 为 `21.5.0 / 100215040`，证书 SHA-256 `6491ec50293dd3dee7a03b74800e09af118fdd0f008725d08b911f850b7d79f4`。原件 SHA-256 `0285ea96a2b924912e8984e45dc0b62907c859475eac5aecce0e52632d571ab2`。版本、签名证据来源及路径见 [身份记录](music/identities.json)。 |
| 4. 开关配置 | **已放** [开关键实读](music/controlled-after-35s.txt)及第 5 项的配置节选。已知载体为 `/data/user/0/com.luna.music/shared_prefs/luna_launch_local_shared_preferences.xml`。上游配置的所有权／远端来源未坐实。完整应用偏好含无关键，仅保留本地。 |
| 5. 具体关法 | **已放** [操作记录](music/toggle-operation.md)、[before 单键](music/launch-preferences.before.key.txt)、[test 单键](music/launch-preferences.test.key.txt)、[设备实读](music/test-live-readback.txt)及 [写入哈希](music/write-verified.txt)。应用停进程时只改布尔键 `enableArtHeapExpandV4`，未用 getprop。完整 XML 原件路径及哈希在单键节选中。 |
| 6. 写回 | **已放** [35 秒后的设备实读](music/controlled-after-35s.txt)，显示 `true`。完整写回 XML 和对应网络拉取日志未保全，写回来源未识别。 |
| 7. 字符串 | **已放** [APK 内相关 ASCII 字符串](music/heap-expand-strings.txt)，按 ZIP 内文件归属导出，覆盖 DEX、SO 及其他入口中明文命中。加密或编码后的字符串不在本次明文扫描范围内。 |
| 8. expand_helper 运行日志 | **不存在于已保全现场**。已有选定 logcat／tombstone 未命中可归属到 heap_expand_v4 的 `expand_helper` 运行日志。二进制字符串与 Perfetto slice 各有独立证据，不能代替对应 tag 的 logcat。 |
| 9. 旧包同库 | **不存在于已保全材料**。旧日用没有同版 21.5.0 的严格安装或运行对照，未找到对应旧 `libsysoptimizer.so` 副本。 |
| 10. 完整墓碑 | **已核对本地原件** `D:/TB371FC-release/clean-rebase-20261104/grok-handoff-20261105/tombstone-15.txt`，PID 18521，SHA-256 `d544a6147bedf71dd91e5c170b48575a2e7c2ab0c122b51ba5944903b3b5db4f`。仓库保留脱敏节选，完整原件包含其他映射和内存内容，按本项要求仅登记路径。 |
| 11. 崩溃前后 maps／全局指针 | **不存在于已保全材料**。没有该 PID 的独立 `/proc/18521/maps` 或调试器 provider 全局指针。现有映射来自该进程的墓碑。离线 provider 命中见既有证据。 |
| 12. 35 秒短测 | **已放** [采集脚本](music/short-test.py)、[开始结果](music/controlled-start.txt)、[时间窗](music/controlled-window.json)、[末端实读](music/controlled-after-35s.txt)。脚本中的序列号已替换，供审阅。原始末端文件还含历史退出记录，完整文件留 D 盘。 |
| 13. V3／V4 镜像、差分与回退 | **已放** [绝对路径、大小、现算哈希](pen/image-inventory.json)、[正向差分清单](pen/delta-result.json)、[V4 → V3 回退清单](pen/rollback.json)。完整镜像与差分原件留在所列路径。下方列出两套 super。 |
| 14. V4 权威构建记录 | **已放** [构建结果](pen/pen-build-result.json)、[集成结果](pen/pen-v4-integration.json)、[容器检查](pen/offline-container-checks.json)。D 盘权威路径见 [环境说明](pen/execution-environment.md)。 |
| 15. 工作根、刷写通道与 Magisk | **已放** [环境说明](pen/execution-environment.md)，对应现有私有仓库中的 [镜像集成](../pen-sharing-compat/integrate-pen-v4.sh) 与 [刷写工具](../tools/flash_candidate_delta.py)。 |
| 16. V3 CoreService 失败 | **已放** [当时的原始 dumpsys 节选](pen/v3-core-start-dumpsys.txt)。开机完成、已记录系统启动请求，服务 `app=null` 且 PID 为空。保存的 `PEN_LOG` 段没有明确拒绝原因。不能把厂商某个拦截分支写成实锤。 |
| 17. 笔与固件 | **实物型号未确认**。设备旧缓存配置为 Lenovo Precision Pen 3，待真笔核对。V4 依赖本机 NVT 输入与既有 CTN730 驱动，不新增或依赖额外的笔固件包。历史 CTN730 缓存固件版本 1041 来自 r99 现场，不能当作 V4 验收读数。 |
| 18. NAS、无线设置与启动日志 | **已放** [APK／容器路径、精确 SHA-256 和完整本地日志路径](comm/component-identities.json)，另附 [启动节选](comm/nas-startup-excerpt.txt)。NAS 位于 `system_ext` 的 OPEX，非 vendor APK。实际挂载后的 APK 路径未做设备确认。 |
| 19. r94-commcenterd.rc | **已放** [全文](comm/r94-commcenterd.rc)。SHA-256 `108b8e120855988fd22d5c7f0201f38b94ee1257d85c0212eaa30177a232a742`。 |
| 20. v17 开关录像和设置 | **仅有用户口述及历史文档**。旧包 v17 共享移动数据曾需切换两次开关，另有保持平板 Wi‑Fi 开启并断开路由器的场景线索。没有当时的录像／可复现完整顺序。`VCOMM_SHARE_NETWORK` 已从源码核对，不能反推出当时点过的是哪个页面。见 [历史对比](comm/v17-communication-history.json)。 |
| 21. 新旧 OplusVirtualComm | **已放** [路径及哈希](comm/component-identities.json)。设备相对路径均为 `/system_ext/priv-app/OplusVirtualComm/OplusVirtualComm.apk`。新包 `7d8a11fe738dab522f7c4d4896aea86f3bef42661c522dfa92fbf7600cbe72df`，v17 `959b381847ec630baab44d670b1502105a18a3fe1f6561a67a94f9325931719b`。新 APK 有本地原件，旧哈希来自当时从分区提取的对比。 |
| 22. 通信验收 | **不适用离线通过**。需真机手机配对、能力协商、建链、路由和手机流量网页实测。通话／短信单独验收。离线可交试跑与回退方案。 |
| 23. 竖屏原图／手势 | **已放** [截图、窗口导出及原脚本路径和哈希](recents/original-paths.json)，附 [多任务复现脚本](recents/capture-multitask.py)、[旋转复现脚本](recents/capture-rotation.py)。原图保留于 D 盘。第 4／8 次右滑后几何一致，旋转轮退回桌面。 |
| 24. 三轮完整 Perfetto | **已放** [A1／B／A2 原始轨迹路径、大小、SHA-256](scheduler/trace-paths.json)。原始 trace 留 D 盘，仓库已有逐帧输入与查询。 |
| 25. 仍卡的主观时间与前台 | **已放** [可关联的负载备注](scheduler/subjective-feedback.md)。现有材料不足以给每次反馈绑定秒级前台应用。 |

## 两套 super 的本地原件

- `D:/TB371FC-release/clean-rebase-20261104/pen-sharing-compat/super-pen-sharing-v3-OFFLINE.img` · SHA-256 `cac703a493dce9be832c3ca81a01b4ca74c47852bc0ad2ff7ac275cb314e5a9e`
- `D:/TB371FC-release/clean-rebase-20261104/pen-sharing-compat/super-pen-sharing-v4-OFFLINE.img` · SHA-256 `31dbe4eafed965806ff4de4242f44103056ada235bdc0dea7acaaaea2470908e`

## 执行边界

汽水线需要给出可回退的应用侧改动、同条件对照、回退触发条件和输入哈希。ART、GC、全局厂商标识保持既有配置。短测证明关闭值曾被写回，持续关闭方式待定位。

笔 V4 需同时核对刷入命令、基线哈希和回退 V3，连接、电量、压感、侧键和应用内输入分开验收。通信、竖屏多任务和流畅度在真机测试前只交试跑方案。流畅度只用第三方重载场景验收。

本目录的内容 SHA-256 见 [SHA256SUMS.txt](SHA256SUMS.txt)。镜像和原始轨迹的绝对路径及哈希见各自清单。
