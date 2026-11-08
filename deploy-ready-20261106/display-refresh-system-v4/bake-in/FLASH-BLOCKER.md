# FLASH BLOCKER — my_product-bakein.img (NOT flashed)

- Timestamp Asia/Hong_Kong: 2026-11-06 16:23:50
- Device: HA1W0JA3 TB371FC ColorOS16 OPD2413_16.0.10.600(CN01) slot=a unlocked=yes
- Img ready: D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\display-refresh-system-v4\bake-in\my_product-bakein.img
- Size: 2228305920
- SHA256: 246c901975dc5eb84c16e16aadcfecb5bcaab790369fe405dc78d1a8c9c479e5
- XML MD5 in tree: 35db38f8c85758c372546c707513642c
- hardware_success_claimed: false
- Flashed: NO

## Probe (fastbootd 2026-11-06)
1. adb reboot bootloader → product=spinel unlocked=yes current-slot=a is-userspace=no
2. fastboot reboot fastboot → is-userspace=yes product=TB371FC unlocked=yes slot=a
3. fastboot getvar partition-size:my_product → FAILED (remote: 'Could not open partition')
4. fastboot getvar partition-size:my_product_a → FAILED (remote: 'Could not open partition')
5. Same for my_product_b; USB then dropped mid-probe
6. Device recovered with fastboot reboot → Android adb online again

## Why stop
Current fastbootd layout does not expose a flashable my_product / my_product_a partition.
Live Android also has no /dev/block/by-name/my_product*; lpdump(super) only shows odm/product/system/system_ext/vendor.
Live /my_product appears as a directory on system (dm-2 ext4), not a separate EROFS mount.
Flashing would risk brick / no-op; per policy STOP after BUILD-OK.

## Exact flash commands (for when partition exists again)
```
adb reboot bootloader
fastboot reboot fastboot
fastboot getvar is-userspace
fastboot getvar partition-size:my_product
fastboot getvar partition-size:my_product_a
# ONLY if size >= 2228305920:
fastboot flash my_product D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\display-refresh-system-v4\bake-in\my_product-bakein.img
# or: fastboot flash my_product_a <same img>
fastboot reboot
adb wait-for-device
adb shell su -c 'touch /data/adb/modules/tb371fc_system_refresh_policy/disable'
adb reboot
# then ABA section 4 EXEC-FOR-CODEX.md
```
Rollback img: D:\TB371FC-release\clean-rebase-20261104\donor-images\my_product.img

## Next unblock ideas
- Confirm Cosy my_* logical partitions via full OTA / payload that recreates them
- Or patch live /my_product/etc/refresh_rate_config.xml via remount/overlay if system-writable path is intentional (NOT done this turn)
- Do NOT flash whole super (HELD_NETWORK_BOOT_INCOMPATIBLE)
## Update 2026-11-06 16:28 Asia/Hong_Kong
Confirmed: `/my_product` is not a mountpoint; stock XML on system tree MD5 7e48f867…; integrated-logicals/system.img matches. Next path = live system-tree bake (LAYOUT-AND-NEXT.md), not this EROFS img.
