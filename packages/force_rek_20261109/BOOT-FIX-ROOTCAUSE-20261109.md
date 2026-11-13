# BOOT-FIX 2026-11-09 — 根因判断（只读，未动设备）

hardware_success_claimed=false
updated: 2026-11-09 15:55 Asia/Hong_Kong
trigger: 用户要求先判断原因、想清楚再处理；禁止在用户手动 FASTBOOT 时自动 reboot。

## 一句话结论
**不是「没刷上 / 半套键盘还在 / 只坏 userdata / 只怪 r108」。**
当前更像是：**整包满刷 + 清数据之后，早期引导约 50s 内被踢回 FASTBOOT**；崩溃原文（pstore/last_kmsg）一直抓不到，所以还不能在「AVB/早期挂载失败」和「首次开机流程被打断/状态不干净」之间一锤定音。
**KEEP 镜像内容本身不是废包**（2026-11-07 delta 刷入曾 boot completed）。

## 已排除（有证据）
1. **没刷进去**：r106 / KEEP 均 385/385 OK；TWRP 侧 vendor/boot/身份核验对得上（KEEP 有 YozoOffice、system 为 ColorOS16）。
2. **半套键盘 VINTF 残留**：干净 vendor 整分区盖过且哈希对齐；其后又满刷 super。
3. **只坏 userdata**：erase → host format → 官方 -Clean wipe → TWRP format data 后仍失败。
4. **只怪 r108**：官方 wipe 后包内 r106 boot 同样回 FASTBOOT。
5. **BCB 残留**：misc 前 2KB 曾为全 0 / 已再清。
6. **缺 vendor_boot**：设备无此分区。

## 关键证据
| 事实 | 含义 |
|------|------|
| KEEP STATUS：2026-11-07 **delta** 刷入后 boot completed + YozoOffice 路径核验 | KEEP 的 super/boot **内容能开机** |
| r106 manifest：`exact full archive has not passed clean first boot` | r106 整包满刷路径本身从未验收 |
| 今日 KEEP **满刷 385** + TWRP format 后仍 ~50s 回 FASTBOOT | 失败点在「满刷/清数据后的引导」，不是「镜像文件坏了」 |
| KEEP+r108 单变量失败时 **unbootable:a=no**（retry 未耗尽） | 不像普通跑完 7 次重试，更像早期被踢回 fastboot / 流程未走完 |
| TWRP format data 提示 *reboot recovery to use /data again*，当时未先回 recovery 再进系统；format 后 /data 已显示约 1.7G used | 数据区可能仍不干净或不一致 |
| 最后一次写盘实验是 **KEEP super + r108 boot** | 盘上 boot 可能与 KEEP super 暂不一致（待只读确认） |
| pstore/last_kmsg 空；本 TWRP 内核无 pstore | 缺崩溃原文 |

## 根因排序（当前）
1. **主因（工作假设）**：满刷 + 清数据后的 **早期引导失败 / 首次开机状态不干净**（含：format data 后未按 TWRP 要求先重启 recovery；可能残留 crypto/metadata 不一致；以及救砖过程中多次自动 reboot 打断观察）。ROM 内容已用「11-07 KEEP 能开」否定「整包废片」。
2. **次因（待证）**：AVB/早期 dm-verity 在「无 pstore」情况下仍可能，但同一套 vbmeta 哈希在 11-07 能开，单靠「镜像 vbmeta 坏」解释力弱；更需对照机内 rollback/unlocked 与其它未刷分区。
3. **已降级**：半套键盘、单纯 userdata erase 不够、r108 独有问题、没刷上。

## 下一步（想清楚后的处理，需你点头后才动；默认不 reboot）
1. **只读**：FASTBOOT 下核对 slot / unbootable / 当前是否仍为 r108 boot 混挂（不 reboot）。
2. **对齐**：若 boot≠KEEP `5b4acefc…`，只刷回 KEEP 包内 `boot_a`（与 KEEP super 配对），`set_active a`，**不自动 reboot**。
3. **数据**：你手动进 TWRP → 再 format data → **先 reboot recovery** → 确认 /data 近空且可挂 → 清 BCB → 再 **只一次** reboot system；我这边只等，不轮询乱重启。
4. 若仍失败：必须拿到 last_kmsg/串口之一，否则停止盲刷。

## 禁止
- 用户已手动进 FASTBOOT 时自动 `reboot`
- 再盲刷另一遍 385 撞同一墙
- 半套 VINTF / 关 verity / 只混 vendor

## Update 2026-11-09 16:12 — 物理键盘是否造成「另外的错误」（离线）

用户假设：刷机/开机时磁吸键盘没拔，结合「键盘读不到」产生新错误；现已拔掉。

### 结论
**拔键盘是对的（下次开机少一个变量），但离线证据不支持「物理键盘插着」才是今天满刷后回 FASTBOOT 的主因。**

### 两层问题要分开
1. **软件半套 VINTF（已证实会砖）**  
   只写入 `vendor.qti.hardware.tinno_keyboard` device manifest、不改 matrix 的 `vendor.mediatek...` → VINTF 失败 bootloop；remount rw `/vendor` 还会打坏 dm-verity。  
   这与键盘**有没有物理贴上无关**——是改了 vendor 分区。  
   今日已满刷 super/vendor，片段不在盘上 → **这条已排除为当前残留主因**。

2. **「键盘读不到」（系统能开、HAL 起不来）**  
   库存 matrix 要 `mediatek` 名，HAL 注册是 `qti` → `tinnokeyboard=stopped`。  
   表现是进系统后键盘无效，**不是**早期 ~50s 掉 FASTBOOT。  
   11-07 KEEP delta 能 boot completed 时，同一套 Tinno 二进制/命名不一致就在镜像里。

3. **物理磁吸贴着**  
   - 用户态 Tinno HAL / `r94-native-keyboard.rc` 都在 `boot_completed` 之后才有意义，到不了那一步就不会因「读不到」把机器打回 fastboot。  
   - 现有 keep-recovery dmesg 只有 USB 充电投票，无 tinno/pogo/HID 键盘探针致 panic 痕迹。  
   - 刷机口是后置 USB；磁吸键盘是另一路，**不能**解释「镜像哈希正确仍 early 回 FASTBOOT」。  
   - 至多：USB 枚举/充电偶发干扰 **主机侧 adb 观察**，造成「以为没起来又 reboot」的误判（与用户抱怨的自动重启叠加）。

### 对下一步的含义
- 键盘保持拔掉：同意，验收开机时继续拔着。  
- **不因此改根因排序**：仍按 BOOT-FIX-ROOTCAUSE 主线（满刷+清数据后早期引导 / format 后未先回 recovery / 可能 KEEP+r108 混挂）。  
- 不因为「已拔键盘」就再盲刷 385。
