# EXEC-FOR-CODEX — refresh_rate_config 写入 my_product（一次做完）

**状态：** deploy-ready 完整 / 本机未刷（flash 闭环未证明）  
**hardware_success_claimed=false**  
**禁止：** Magisk bind oplus-services.jar

## 0. 已知事实（勿重探）
- Magisk XML-only ABA PASS：MD5 35db38f8c85758c372546c707513642c；Version=20260107；Preferred/Default [4,4,2,4]；微信/抖音/汽水 PickRate=144
- defaultRateId 必须是连字符元组 4-4-2-4
- Preferred 来自 systemui item，不是裸 config
- flash-candidate 当前 HELD_NETWORK_BOOT_INCOMPATIBLE → 不要刷整包 super-cleanbase；只做 my_product 单分区
- Qin WSL 2026-11-06 报 WSL_E_DISK_CORRUPTED → 本机无法 mkfs.erofs；Codex 用 Linux 构建机执行第 2 节

## 1. 输入（已齐）
| 文件 | 路径 |
|------|------|
| 规范 XML | deploy-ready-20261106/display-refresh-system-v4/bake-in/refresh_rate_config.xml |
| stage 副本 | .../rom-stage/refresh_rate_config.xml |
| 树补丁 | .../rom-stage/patch_my_product_tree.py |
| EROFS 打包 | .../rom-stage/rebuild_my_product_erofs.sh |
| 解包树 | donor-tree-case/my_product/（stock MD5 7e48f867e573a1e207471805e3d03902） |
| 镜像 | donor-images/my_product.img（EROFS ~2.05GiB） |
| fastboot | flash-candidate/tools/fastboot.exe |

## 2. 构建（Linux）
```bash
cp -a donor-tree-case/my_product /work/my_product-bakein
python3 deploy-ready-20261106/display-refresh-system-v4/rom-stage/patch_my_product_tree.py /work/my_product-bakein
# 期望 MD5 35db38f8c85758c372546c707513642c

bash deploy-ready-20261106/display-refresh-system-v4/rom-stage/rebuild_my_product_erofs.sh \
  /work/my_product-bakein /work/my_product-bakein.img
# 若压缩机与 donor 不一致：用 dump.erofs 读 donor 后改 -z 参数重打
```

## 3. 刷写（仅 my_product / fastbootd）
前置：已授权刷机；备好 donor-images/my_product.img 回滚。

```bash
adb reboot fastboot
fastboot reboot fastboot
fastboot flash my_product /work/my_product-bakein.img
# 或：fastboot flash my_product_a /work/my_product-bakein.img
fastboot reboot
```

刷后禁用 Magisk refresh（否则仍是 bind，验不了 ROM）：
```bash
adb shell su -c 'touch /data/adb/modules/tb371fc_system_refresh_policy/disable'
adb reboot
```

## 4. ABA（无 Magisk refresh）
- md5sum /my_product/etc/refresh_rate_config.xml → 35db38f8c85758c372546c707513642c
- dumpsys oplusscreenmode → Version 20260107；mDefaultRateId=[4,4,2,4]；PreferredRefreshRateId=[4,4,2,4]；control panel:4
- 热启微信/抖音/汽水 → mCurrentPickRate=144
- luna heap 模块保持独立

## 5. 回滚
```bash
fastboot flash my_product donor-images/my_product.img
fastboot reboot
# 可恢复 Magisk refresh：product-config/magisk-module
```

## 6. 本轮停线
- 材料+脚本已落盘；未产出 my_product.img（无可用 mkfs.erofs）；未 fastboot
- 跟手并行：sf-duration-144-trial


---

## 7. APPEND 2026-11-06 Asia/Hong_Kong 16:28 — my_product **partition flash is WRONG** for this live build

Do **not** destroy prior sections; this overrides §3 flash target for OPD2413_16.0.10.600(CN01) as running on HA1W0JA3.

### Layout (proven)
- Live `/my_product` is a **directory on system** (`/dev/block/dm-2` = `system_a` ext4), **not** a separate EROFS mount.
- `lpdump` / fastbootd / `/dev/block/by-name` / mapper: **no** `my_product` / `my_product_a`.
- Stock XML without Magisk: MD5 `7e48f867e573a1e207471805e3d03902` (200296 B) at `/my_product/etc/refresh_rate_config.xml`.
- Same stock file inside `integrated-logicals/system.img` and `base-ext4-UNADAPTED/system.img`.
- Cosy props/fstab still *name* my_* logicals, but this super never created them (merged into system).

### BUILD-OK artifact status
- `bake-in/my_product-bakein.img` built OK (SHA256 `246c9019…`) but **FLASH-BLOCKER** — nowhere to flash.
- Keep img only if future OTA restores Cosy my_* partitions.

### Correct long-term bake for THIS build
1. **Preferred next:** live remount write of proven XML into system tree — see `bake-in/LAYOUT-AND-NEXT.md` + `bake-in/live-bake-refresh-xml.sh`.
2. Magisk XML-only remains valid **interim** (ABA PASS) until live bake ABA.
3. Offline: patch `my_product/etc/refresh_rate_config.xml` inside matching **system.img** then `fastboot flash system` — only if live bake blocked; do **not** flash whole super (still HELD_NETWORK…).
4. Still **forbid** Magisk bind of `oplus-services.jar`.

hardware_success_claimed=false
