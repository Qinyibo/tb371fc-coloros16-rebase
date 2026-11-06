# 汽水音乐有限处理 · 可部署草案

## 结论（先读）

强候选已闭合到**应用侧 `libsysoptimizer.so` 单点偏移**：

| 项 | 值 |
| --- | --- |
| 选中 provider | `offset_provider_api31_huawei` |
| 返回位图对象偏移 | `0x2f0`（文件偏移 `0x7209c` 处 `mov w0,#0x2f0`，唯一） |
| 本机 ART RegionSpace 期望 | `0x308`（live/mark getter） |
| 差值 | 24 字节，与墓碑连贯布局一致 |
| so 内是否存在 `0x308` 常量 | **否**（`api31_till_last` 槽位返回 `0x2e8`，同样不对） |

`enableArtHeapExpandV4` 可在停进程后写成 `false` 并短测无崩溃，但约 35s 正常前台后被应用写回 `true`。**不能把单次改 prefs 当成持久修复。** 写回来源未保全（DEX 可见 `ArtHeapExpandOptimizer`／`setEnableArtHeapExpandV4`／`luna_launch_local_shared_preferences`）。

**推荐部署路径 A（主）**：把唯一指令 `0x2f0` → `0x308`，保留扩展意图、对齐 ART。  
**回退路径 B**：把 `HeapExpandV4_applyNative` 开头改成 `mov w0,wzr; ret`（彻底不扩展）。  
**应急路径 C**：prefs 看门狗强制 `false`（仅 A/B 都无法落地时；默认关闭）。

不改 `libart`、不改 GC 属性、不改厂商标识。

## 输入哈希

- 原 `libsysoptimizer.so` SHA-256 `e8357c10cef28edb36ad59faeec51d120c9ae41f04ff3de8f5874349dc5f7ec3` BuildId `5ba6754a5e6f6684715e45f17c582f47de746879`
- 补丁后（A）SHA-256 `be0565463b741685bdf95803fbb9d5de57832ad862b5e66555df2df7ecc66416`
- 补丁后（B）SHA-256 `2dc3bda37442e36f9fd6d3b2a19aec427e59c0393449f0ffb433095c94cf0b4e`
- APK `0285ea96…`／证书 `6491ec50…`／tombstone-15 `d544a614…`
- libart `63ed6aa8…`

工件：

- `libsysoptimizer.so.original`
- `libsysoptimizer.so.patched-0x308`（A）
- `libsysoptimizer.so.patched-disable-apply`（B）
- `patch-bitmap-offset.json`／`patch-disable-apply.json`
- Magisk 模块 zip：`tb371fc_luna_heap_offset_fix-v1.zip`（内嵌 A）

## 补丁 A 字节级

- 文件偏移 = VA = `0x7209c`（首 LOAD `p_vaddr==p_offset`）
- 旧：`00 5e 80 52`（`mov w0,#0x2f0`）
- 新：`00 61 80 52`（`mov w0,#0x308`）
- 全库仅 1 处 `mov w0,#0x2f0`

## 补丁 B 字节级

- 符号 `Java_com_bytedance_sysoptimizer_heap_HeapExpandV4_applyNative` @ `0x6c6ac`
- 前 8 字节旧：`fd 7b bf a9 fd 03 00 91`
- 新：`e0 03 00 2a c0 03 5f d6`（`mov w0,wzr; ret`）

## Codex 执行步骤（A，推荐）

工作根：`D:/TB371FC-release/clean-rebase-20261104`。设备需 Magisk 31.1 root。

1. 确认设备上活库哈希仍为 `e8357c10…`：
   ```
   adb shell '/debug_ramdisk/su -c "find /data/app -name libsysoptimizer.so | while read f; do echo $f; sha256sum $f; done"'
   ```
   若哈希已变（应用更新），**停止**，回我方重新对偏移（本草案绑定该 BuildId）。
2. 推送补丁库并替换（示例）：
   ```
   adb push libsysoptimizer.so.patched-0x308 /data/local/tmp/libsysoptimizer.so.patched
   adb shell '/debug_ramdisk/su -c "am force-stop com.luna.music; F=$(find /data/app -path \"*com.luna.music*\" -name libsysoptimizer.so | head -1); cp -a \"$F\" \"$F.bak-e8357c10\"; cp /data/local/tmp/libsysoptimizer.so.patched \"$F\"; chmod 755 \"$F\"; sha256sum \"$F\""'
   ```
   期望输出哈希 `be056546…`。
3. 可选：安装 Magisk 模块 zip（同补丁），开机 `post-fs-data` 自动覆盖；应用商店更新后若哈希回到原值会再次覆盖。
4. **不要**同时改 prefs；A 生效时扩展仍可跑，但偏移正确。

### 同条件对照（必须）

| 轮 | 条件 | 动作 | 通过标准 | 失败→回退 |
| --- | --- | --- | --- | --- |
| T0 | 补丁前备份在 | 记录活库哈希／tombstone 基线 | 哈希=e8357c10 | — |
| T1 | A 已替换 | 冷启动汽水，正常听歌／切歌 10 分钟，不主动压 GC | 无 `HeapTaskDaemon` SIGSEGV；`maps` 中 region live bitmap 与堆扩展若发生，不出现 `this=region+0x2f0` 错位崩溃 | 立刻执行回退 |
| T2 | A 已替换 | 复现曾触发扩展的操作（若可知）；抓 logcat `expand_helper`（可能仍无 tag，不强制） | 无同类 tombstone | 回退 |
| T3 | 若 A 可疑 | 换 B（disable apply）重做 T1 | 无扩展、无该类崩溃 | 回退原 so |

### 回退

```
adb shell '/debug_ramdisk/su -c "am force-stop com.luna.music; F=...; cp -a \"$F.bak-e8357c10\" \"$F\"; sha256sum \"$F\""'
```
期望回到 `e8357c10…`。Magisk 模块则卸载模块并重启。

### 否定条件（出现则不得宣称成功）

- 活库 BuildId／SHA 与草案不一致仍强行打补丁
- 改了 ART／GC／ro.product.*／调度叠层
- 仅改 prefs 且未处理写回却宣称持久修复
- 无 T1 对照就写 hardware_success

## prefs 应急（C）

仅当无法写 so 时：`am force-stop` 后改  
`/data/user/0/com.luna.music/shared_prefs/luna_launch_local_shared_preferences.xml`  
键 `enableArtHeapExpandV4`→`false`，并启用模块内 `enable-prefs-watchdog` 旗标。已知应用会写回；看门狗是折中，不是根治。
