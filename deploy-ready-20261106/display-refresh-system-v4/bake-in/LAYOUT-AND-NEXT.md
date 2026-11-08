# LAYOUT-AND-NEXT — TB371FC ColorOS16 refresh bake path

- Timestamp Asia/Hong_Kong: 2026-11-06 16:28
- Device: HA1W0JA3 TB371FC OPD2413_16.0.10.600(CN01) slot=_a unlocked=orange
- Magisk refresh module: tb371fc_system_refresh_policy v4d still ACTIVE (bind)
- hardware_success_claimed: false
- Flashed this turn: NO

## Mount facts (live)

| Path | Fact |
|------|------|
| `/` | `/dev/block/dm-2` = `system_a` ext4 **ro** (remount,rw works on this unlock) |
| `/my_product` | **NOT a mountpoint** — directory on system (inode on dm-2) |
| Magisk bind | `sda15 (userdata)` → `/my_product/etc/refresh_rate_config.xml` (file bind only) |
| `/product` | `/dev/block/dm-1` product_a (tiny ~24M) — unrelated to refresh XML |
| super (lpdump) | **only** odm_a, product_a, system_a, system_ext_a, vendor_a — **no my_*** |
| by-name / mapper | no `my_product*`; mapper = odm/product/system/system_ext/vendor `_a` |

Props still advertise Cosy-style `ro.build.oplus_ext_partitions` / `ro.product.ab_ota_partitions` including `my_product`, but **this live super does not materialize those logicals**. Donor `fstab.qcom` expects `my_product` logical → `/mnt/vendor/my_product` then bind to `/my_product`; live boot skipped that and kept the tree that was **merged into system.img**.

## Where stock XML lives (without Magisk)

| Source | MD5 | Size | Notes |
|--------|-----|------|-------|
| Live after `su -mm` umount Magisk bind | `7e48f867e573a1e207471805e3d03902` | 200296 | 2026-09-11 22:28 |
| `integrated-logicals/system.img` `/my_product/etc/...` | same | 200296 | ext4 ~9.5G — matches live layout |
| `base-ext4-UNADAPTED/system.img` same path | same | 200296 | same |
| `donor-tree-case/my_product/etc/...` | same | 200296 | Cosy extract of separate img |
| Magisk / bake-in proven XML | `35db38f8c85758c372546c707513642c` | 198373 | ABA PASS |

`find` under `/system /product /odm /vendor /my_*` → **only** `/my_product/etc/refresh_rate_config.xml`.

## Magisk module (current)

```
/data/adb/modules/tb371fc_system_refresh_policy/
  module.prop          v4d
  post-fs-data.sh      mount -o bind $MODDIR/refresh_rate_config.xml → /my_product/etc/refresh_rate_config.xml
  refresh_rate_config.xml   MD5 35db38f8…
```

## Why `my_product-bakein.img` cannot be flashed

- BUILD-OK produced EROFS `my_product-bakein.img` (SHA256 `246c9019…`, 2228305920 B) from Cosy donor `my_product.img`.
- fastbootd: `partition-size:my_product` / `my_product_a` / `_b` → **Could not open partition** (see FLASH-BLOCKER.md).
- Live confirms: no partition, `/my_product` is system-folder. Flashing that img has **nowhere to land**.

Keep the img only as artifact if a future Cosy/OTA rebuild re-adds my_* logicals. **Wrong target for OPD2413_16.0.10.600(CN01) live.**

## Strategy decision

| Option | Verdict |
|--------|---------|
| A patch folder inside **system.img** / live system tree | **YES — matches how this build ships my_product** |
| B Magisk XML-only long-term | Valid **interim** (ABA PASS); not ROM bake |
| C Cosy my_company / odm / overlayfs product | **No evidence** of a writable alternate home for this XML; `/my_company` empty; overlays consume `/my_product/overlay` from the same system tree |

### Recommended ONE next deploy step = **A-live** (in-place system tree bake)

Do **not** flash 9.5G system yet. Remount proved writable (`touch /my_product/etc/.write_test_refresh` OK; file removed). Replace stock XML with Magisk-proven file, restore SELinux, disable Magisk module, reboot, ABA.

Script: `live-bake-refresh-xml.sh` (same folder) + host driver notes below.

### Offline system.img flash (A-offline) — deferred

Only if live bake blocked: patch `integrated-logicals/system.img` (or a dump of **current** live system) at `my_product/etc/refresh_rate_config.xml`, flash `system`/`system_a` only. Risks: large image, must match live network/base (flash-candidate still HELD_NETWORK_BOOT_INCOMPATIBLE for whole super), vbmeta/AVB. Prefer live path first.

## Exact next commands (deploy — not run this turn)

From Qin (device online, Magisk still active):

```bat
adb -s HA1W0JA3 push D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\display-refresh-system-v4\bake-in\refresh_rate_config.xml /data/local/tmp/refresh_rate_config.xml
adb -s HA1W0JA3 push D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\display-refresh-system-v4\bake-in\live-bake-refresh-xml.sh /data/local/tmp/live-bake-refresh-xml.sh
adb -s HA1W0JA3 shell su -c "sh /data/local/tmp/live-bake-refresh-xml.sh"
adb -s HA1W0JA3 reboot
adb -s HA1W0JA3 wait-for-device
```

Then ABA (Magisk refresh **disabled** by script):

```bat
adb -s HA1W0JA3 shell "su -c 'md5sum /my_product/etc/refresh_rate_config.xml; mount | grep refresh_rate || true; dumpsys oplusscreenmode | head -80'"
```

Expect MD5 `35db38f8c85758c372546c707513642c`, no Magisk bind line, Preferred/Default `[4,4,2,4]`, warm PickRate=144.

Rollback:

```bat
adb -s HA1W0JA3 push D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\refresh_rate_config.xml /data/local/tmp/refresh_rate_config.stock.xml
rem stock copy above is MD5 7e48f867… size 200296 — or pull from donor-tree-case
adb -s HA1W0JA3 shell su -mm -c "mount -o remount,rw /; cp -f /data/local/tmp/refresh_rate_config.stock.xml /my_product/etc/refresh_rate_config.xml; chmod 644 /my_product/etc/refresh_rate_config.xml; chown root:root /my_product/etc/refresh_rate_config.xml; restorecon -v /my_product/etc/refresh_rate_config.xml; sync; mount -o remount,ro /; rm -f /data/adb/modules/tb371fc_system_refresh_policy/disable"
```

## Risks

- Live remount write mutates system partition content; survives Magisk removal; **does not** survive full system reflash/OTA.
- Must `su -mm` umount Magisk bind before overwrite, else you rewrite the Magisk file on userdata.
- SELinux Enforcing — need `restorecon` (`u:object_r:system_file:s0`).
- Free space ~99M; new file smaller than stock — OK.
- Do **not** flash `my_product-bakein.img`. Do **not** flash whole super.

## system flash needed?

**No** for the recommended next step (live bake). Offline `fastboot flash system` only if live bake fails or for packaging a reflashable ROM image later.
