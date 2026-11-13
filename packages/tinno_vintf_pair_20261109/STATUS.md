# TB371FC tinno VINTF Magisk — STATUS (2026-11-09 evening)

## Result
PASS (software): Magisk module + boot overlay persist; tinno HAL registers after reboot.
Device: HA1W0JA3 / OPD2413_16.0.0.210(CN01) / slot a
Keyboard physical attach: NOT tested yet (keep unplugged until you say).

## Live verify (after overlay boot)
- init.svc.tinnokeyboard=running
- lshal: vendor.qti.hardware.tinno_keyboard@1.0::ITinnoKeyBoard/default
- /vendor/etc/vintf/compatibility_matrix.xml → vendor.qti.hardware.tinno_keyboard
- fragment present under /vendor/etc/vintf/manifest/
- Magisk 30.7 loaded module tb371fc_tinno_vintf_pair (this boot: NOT safe-mode)

## Artifacts (Qin)
Dir: E:\youxikaifa\work\today-20261109\kb-vintf-magisk\

| File | SHA256 |
|---|---|
| tb371fc_tinno_vintf_pair.zip | 16E3F4FF045D824482EFCD5CE92251129A8FCB2326F38BC36978AD6CF3AB2078 |
| boot-r108-resx-magisk.img (plain Magisk 30.7) | 62428F25F857BCC15FE8AB4A3A18148C5B37723109DE60F974C470188839A825 |
| boot-r108-resx-magisk-tinno.img (Magisk + overlay.d init.tinno_vintf.rc) **FLASHED** | 1C573C2E6B83C212A217884F771A9AE722D3956B51B8F2075C10499D1E86C2DB |
| stock rollback boot-r108-resx.img | F5F446047721E788451FBDE8D984A8E3DCA0AC21E18E85F9F15839C6289B1F13 |

## Persistence design
1. Magisk module `tb371fc_tinno_vintf_pair` (systemless bind over /vendor VINTF pair).
2. `/data/adb/tinno_vintf_fix.sh` + `service.d` copy: late remount + restart hwservicemanager if needed.
3. Boot overlay.d `init.tinno_vintf.rc` starts that script on boot_completed (backup when Magisk safe mode disables modules).

## Known Magisk issue on this device
Earlier boots: Magisk `* Safe mode triggered` every time (volume-down key combo false positive) → modules got `disable`.
Mitigation: overlay.d late fix + SELinux `vendor_configs_file` on bind sources.
If safe mode returns, overlay path still applies VINTF after boot_completed.

## Safety kept
- No vendor remount-rw / no vbmeta / no verity disable
- No KEEP flash
- One reboot per flash step; no auto-reboot from FASTBOOT beyond flash scripts
- Keyboard left unplugged for this validate

## Next (needs you)
1. Physically attach magnetic/Tinno keyboard and confirm input.
2. If Magisk app asks for additional setup, open Magisk 30.7 once.