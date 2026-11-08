# SF duration Magisk 试验 — BOOT HANG，不采纳

**时间:** 2026-11-06 Asia/Hong_Kong  
**hardware_success_claimed=false**

## 结果
安装 	b371fc_sf_duration_144 并 reboot 后：
- db 显示 device，但 sys.boot_completed 长时间为空
- wm/settings 服务不可用（卡在开机动画/SystemServer 未完成）
- 判定：**开机卡住**，与成组 debug.sf.use_phase_offsets_as_durations=1 + 144 duration / 改写 high_fps_* 相关

## 处置（已执行）
1. 	ouch /data/adb/modules/tb371fc_sf_duration_144/disable
2. db reboot
3. 恢复：boot_completed=1，wm=1840x2944
4. 模块保持 **disable**；勿再启用同配方 Magisk

## 恢复后实机
- refresh Magisk 仍启用，XML MD5 35db38f8…，PickRate/Preferred 144 OK
- SF 回到 pp duration=8888888 / SF duration=10944444 / mWorkDuration=8.89
- dynframe / VRR TouchIdle-off 仍 disable
- blackscreen ring 已重启：lackscreen-ring/ring-20261106-153325.log

## 结论
**Magisk/runtime 改 SF duration props 在本机 ColorOS16 不安全（开机卡住）→ 路径关闭。**  
跟手 duration 对齐只能走 **离线 vendor 镜像 bake**（可回滚 fastboot），且必须在刷写前用 VM/second device 验 boot；本机 Qin WSL 损坏暂不能 mkfs，且 vendor 改动超出当前 my_product-only bake-in 范围。

## 已选下一工程师步骤（不甩用户）
1. **主线继续：** 按 display-refresh-system-v4/EXEC-FOR-CODEX.md 完成 my_product refresh XML ROM bake（Linux mkfs.erofs → fastboot flash my_product → 卸 Magisk refresh → ABA）。
2. **跟手 duration：** 在 donor endor/build.prop 上准备 **离线** 144 对齐 duration 补丁草案（成组 high_fps_* 正 duration），放入 sf-duration-144-trial/VENDOR-BAKE-DRAFT.md；**禁止**再 Magisk 实机试。待有可回滚 vendor 刷写闭环后再上第二台/VM 验 boot。
3. 并行只读：从 donor libsurfaceflinger*.so / oplus SF 扩展搜常量 8888888 来源（离线 strings），写入同一目录，仍不 jar-bind。
