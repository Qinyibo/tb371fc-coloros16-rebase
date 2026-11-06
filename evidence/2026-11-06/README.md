# Grok 核验材料 · 2026-11-06

这批材料对应 TB371FC ColorOS 16 `.600` 重适配。当前工作状态见 [STATUS.md](../../STATUS.md)。[证据清单](manifest.json)标明来源、选取方式和 SHA-256。

| 要核对的问题 | 证据入口 |
| --- | --- |
| 汽水音乐 21.5.0 的原生崩溃 | [墓碑节选](music/tombstone-excerpt.txt)、[crash buffer 对应行](music/crash-buffer-fatal.txt)、[故障指令](music/art-fault-site.asm)、[地址计算](music/fault-address-arithmetic.json) |
| 位图对象从哪里开始、为什么差 24 字节 | [布局事实](music/art-layout/layout-facts.json)、[故障对象字值](music/art-layout/crash-bitmap-near.hex.txt)、[健康对象字值](music/art-layout/healthy-bitmap-once.hex.txt)、[ART 构造和 getter](music/art-layout/)、[应用探测与移动指令](music/app-probe/) |
| 扩展事件与 GC 的顺序 | [Perfetto 导出](music/music-gc-expansion.csv)、[查询](music/music-gc-expansion.sql)、[现场范围](music/music-evidence-facts.json) |
| 后来一次退出 | [ANR 事实](music/later-anr-facts.json)。输入超时 5 秒、堆栈采集超时。两次线程等待快照各有 482 个线程在 do_signal_stop，信号发送者未知 |
| 前台调度的开启、撤出、恢复 | [协议和起止](scheduler/protocol.json)、[A1](scheduler/A1-controller-on/)、[B](scheduler/B-controller-off/)、[A2](scheduler/A2-controller-on/)。各轮附用于计算 P95 的逐帧 CSV、SQL、最慢抖音帧附近的线程状态、工作负载和资格判断 |
| 手写笔、通信和竖屏后台 | [V4 源码和离线状态](../../pen-sharing-compat/)、[v17 通信镜像对比](hardware/v17-vnet-comparison.json)、[竖屏复现范围](hardware/recents-observations.json) |

## 解释边界

- `libsysoptimizer` 的探测逻辑按当前 ART 指令离线重放，选中内部名 `api31_huawei` 的 provider，返回 `0x2f0`。当前与旧 ART 的 `RegionSpace` getter 取 `0x308`，和故障对象位置差 24 字节相符。应用移动了 128 字节的对象，位图数据另行复制。历史现场的写入尚未实时追踪。`0x80` 是从二进制重建的对象占用，缺少 DWARF `sizeof`。健康样本来自另一个进程，单次读非原子。
- 汽水音乐 APK 版本 21.5.0 / 100215040，安装来源为 `com.heytap.market`，证书 SHA-256 `6491ec50293dd3dee7a03b74800e09af118fdd0f008725d08b911f850b7d79f4`。旧 ROM 上同版同路径对照缺失。扩展标记来自 Perfetto，缺连续崩溃前 main logcat。关闭应用私有扩展开关的短测观察到 1 GB 堆且窗口内无新崩溃，应用之后又开启该开关。
- [当前 Dalvik 实读](music/current-dalvik-properties.txt)可和[旧镜像静态属性](music/old-art-static-properties.json)并排检查。旧运行期属性覆盖未知。当前 libart/libartbase SHA-256 分别为 `63ed6aa8ffbc82db163faaaf5bd1cf0e3bdf1138af7e0d32bab80283e6e2452a`、`af44dae6842900f4a5ae91d38f055b0ca81c52740975883f5bce7cc3875a8c40`。旧镜像对应为 `16c6d07f5baaff155478664adbcd773386cfd9aff4bdd856652406c749e9c187`、`6e84d07e71834300e6b71aae9ab45f70c6bd09ce7a43f415394f23e544d1ac5c`。
- 调度数据来自 FrameTimeline，按 app、upid、surface frame token 去重，保留最大 duration，单位 ns。未采集 gfxinfo/framestats，未丢弃完整预热轮，未记录页面或内容身份。每段 16 次显式抖音启动，GPU level 4、四扬开启。A1 仍观察到汽水音乐 CPU 活动。抖音 P95 40.00 / 17.89 / 17.13 ms 不足以裁决永久调度改动。
- V4 仅离线构建。平板输入、真笔、真手机共享、游戏兼容和长期流畅度都缺本轮验收。

完整墓碑、任意堆内存、原始 Perfetto、设备日志、截图、APK/SO 与固件留在 D 盘。这批文件保留核验所需的进程号、时间和地址，已选去身份、账号、触点和无关进程信息。
