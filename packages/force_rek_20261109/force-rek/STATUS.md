# Force REK pack/flash/sleep-wake — RESULT

Asia/Hong_Kong 2026-11-09 ~20:28

## Boots
- Magisk: `E:\youxikaifa\work\today-20261109\boot-diag\boot-r108-force-rek-magisk.img`
  SHA256 `71340E8D8751C9951844C4BDBEFB1BDB49F75EE8F41F06F4B33811B9A9F5AA3E`
- Stock archive: `...\boot-r108-force-rek.img`
  SHA256 `54471AF4DDCEC36E98BE28C4A73C7B88E637A6D5395564A189AD7A4EADCA4994`
- Image: SHA256 `2CB1B19D7D7C3480E59AA3B255F8A8686A923ACB5CE9B1750D82FF7625AD6D80`

## Flash
- `fastboot flash boot_a` Magisk image only → OK
- one reboot → `boot_completed=1`
- uname: `tb371fc-offline@r108-force-rek` #45

## Sleep/wake verdict (panel-force-rek-20261109-202747)
```
R10x_FORCE_REK_PRE_STATE=0xA0
R10x_FORCE_REK_SENT cmd=0x23 0x00
R94_REAL_READY state=0xA1 retry=0
R10x_FORCE_REK_STATE_OK >=REK
R94_NATIVE_COMPLETE_COMMITTED real_REK_verified IRQ_OPEN
```
- R107_ count in full dmesg: **0**
- Power after wake: `mWakefulness=Awake`, dumpsys `mScreenState=ON` (one brightness field 8191.0)
- su actual_brightness re-read interrupted by Qin disconnect after capture; kernel path succeeded

hardware_success_claimed=false
