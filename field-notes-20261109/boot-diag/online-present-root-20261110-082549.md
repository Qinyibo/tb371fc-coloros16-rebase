# TB371FC online-bit flap + POGO present=0 root dig
timestamp: 2026-11-10 ~08:18–08:25 Asia/Hong_Kong
device: HA1W0JA3 / OPD2413_16.0.0.210(CN01) slot _a / Force REK Magisk boot kept
Qin machineId: d034a1ca-7f3e-4320-ba7e-4a4db4e6fc6b
USB-C during dig: **still Source attached** (ADB over USB)
hardware_success_claimed=false
limits honored: no GPIO write; no vendor remount; no unpaired VINTF; no new Magisk/boot flash; power/control left **auto**

## Sync
- Copied `kb-batt-bypass-20261109-231827.md` from box → Qin cwd, then into `E:\youxikaifa\work\today-20261109\boot-diag\`

## Live baseline (2026-11-10 08:19 HKT)
| metric | value |
|---|---|
| tinno / lshal | **PASS** (tinnokeyboard running; ITinnoKeyBoard/default) |
| dc POGO present/online | **0 / 0** (voltage_now empty; current_max=0; input_suspend=0) |
| usb | present=1 typec_mode=**Source attached**; battery charging from USB path; Dock powered=**false** |
| HID 5-0060 / 0018:17EF:6175 | kb_status=**Not connected**; version=**HOST_MCU:80, online:0** |
| i2c_hid PM | control=auto; runtime=**active** (would not autosuspend in 20s) |
| Lenovo input nodes | **none** |
| hall OCH8801 (3-0018) | **driver unbound**; mLidState=LID_ABSENT / UNDOCKED |

## 1) Why `online` self-clears (MCU bit0)

### Gate (kernel, Force REK / audit tree `i2c-hid-core.c`)
- Status report `inbuf[2]==0x06` → `kb_connect = inbuf[3] & 0x01`
- `kb_connect==0` → `hidinput_disconnect`; `==1` → `hidinput_connect`
- `kb_batt_level=inbuf[9]` is **telemetry only** (not a gate) — confirmed prior report; **do not advise charging the keyboard** (user: not a chargeable pack)

### How MCU is powered/woken (software)
- `mcu_resume_gpio` is driven by `kb_i2c_hid_resume` / `kb_i2c_hid_suspend` (Spruce OSPURCET-1235), hooked from `kb_hid_resume` / `kb_hid_suspend` (screen on/off path), **not** from generic `i2c_hid_runtime_*` alone
- Resume: GPIO **HIGH** then I2C PWR_ON; Suspend: GPIO **LOW** then PWR_SLEEP
- If `g_already_sleep==false`, resume helper returns -1 (no re-pulse)

### Live probes this morning (reversible)
1. `power/control=on` while already **active** → **no** online:1 flicker, **no** dmesg KB lines, dc stayed 0/0 → reverted to **auto**
2. Attempt force-suspend (autosuspend_delay=0, even with tinno **stopped**) → runtime stayed **active** 15–20s; resume-on still no flap → tinno restarted; control left **auto**
3. Contrast **2026-11-09 ~23:05**: when runtime was **suspended**, `control=on` produced brief `online:1` / `kb_batt_level:0` / `KB:0` then Dis-connected (while dc still 0)

### Historical proof keyboard MCU can speak fully (unsafe path — DO NOT REPEAT)
`kb-gpio-hold-host.log` (userspace mcu_resume hold — known bootloop risk):
- Intermittent `MCU:80,KB:28,TP:3,BT:34,online:1` with **dc_p=0 dc_o=0**
- Then flaps to `Not connected` / `HOST_MCU:80, online:0` within seconds
- **Interpretation:** tablet can talk to a live pack MCU when resume line is forced; link is **not** sustained without proper power sequencing. **dc/present never required for a brief online:1**, but sustained use historically assumed POGO power + proper resume — GPIO hold is **not** an allowed long-term fix.

### Why flap
MCU clears `inbuf[3]` bit0 when it drops offline. Ephemeral wake (runtime/I2C power or short resume) yields seconds of `online:1` then clear. Without sustained tablet-side POGO/MCU power path, bit0 cannot stay set. Today's stuck `runtime=active` prevented even the brief resume pulse.

## 2) Why `dc/present` never asserts

### How present is computed (`smb5-lib.c`)
`c
smblib_get_prop_dc_present():
  read DCIN_BASE+INT_RT_STS → DCIN_PLUGIN_RT_STS_BIT
`
- Pure **hardware IRQ status** — userspace/Magisk/tinno **cannot** forge it
- `input_suspend=0` live → not software-suspended

### Does USB-C Source **block** present?
- **No software mask found** that clears/hides `DCIN_PLUGIN` because USB is attached
- `dc_plugin_irq_handler` treats `dcin_present && !vbus_present` specially for wireless/AICL path; when both present it takes the else branch — still updates `dc_psy` from the hardware bit
- DT `lenovo,pogo-5v` on live device: **absent** (`pogo5v=NO`) — only changes wireless-style CP voting when DCIN-only; **does not** gate `present`
- **Conclusion:** USB-C Source is **not proven** as a software blocker for `present`. It remains a useful **electrical control** (retest with USB unplugged / wireless adb) but should not be blamed as the primary software cause while `voltage_now` is empty

### Practical meaning
SMB5 never sees DCIN voltage on the tablet POGO sense rail → `present` stays 0. Matches user direction: treat as **tablet-side detect/power path** (keyboard USB + magnetic contacts asserted OK by user).

## 3) Regression timeline hypothesis (why it used to work)

| era | software | physical | notes |
|---|---|---|---|
| Pre-ColorOS16 / stock working (user) | stock tinno/VINTF paired | presumed DCIN + MCU stable | baseline “以前都可以” |
| ColorOS16 full flash / half-VINTF experiments | tinno **unpaired** → HAL exit 1 / bootloop risk | unknown; digs later always show present=0 | bricks from **unpaired VINTF**, not r108 boot itself (memory) |
| Magisk `tb371fc_tinno_vintf_pair` | software **PASS** restored | present=0 unchanged | proves further VINTF churn will not fix attach |
| Force REK Magisk boot #45 | Lenovo i2c-hid + mcu_resume path present in Image | present=0; brief online only on resume pulse / unsafe GPIO | keep this boot; do not flash new without parent OK |
| 2026-11-09 evening digs | tinno OK | PM-on flicker online:1 KB:0 then drop; hall unbound | same physical fail class |
| 2026-11-10 morning (this dig) | tinno OK | **no** flicker (runtime stuck active); HOST_MCU:80 online:0; present=0 | soft wake path currently inert |

**Best explanation for “以前都可以 / 现在坏了”:** after the ColorOS16 + vendor/VINTF churn window, **userspace keyboard stack was restored**, but the **tablet POGO→DCIN electrical detect never comes back** in any post-flash dig. Concurrently, MCU wake depends on `mcu_resume` / I2C power pulses that only yield **seconds** of `online:1`. Hall driver missing is a **secondary** lid-UX regression, not the connect gate. USB-C almost always attached during ADB sessions is a confounder for electrical retest, **not** a proven software present-blocker.

## 4) Recommended long-term fix order (stable)

1. **Hardware / tablet POGO→DCIN continuity (PRIMARY)**  
   - With keyboard magnetically seated, verify tablet-side POGO power-sense pads actually deliver voltage into SMB5 DCIN (multimeter / contact cleaning on **tablet** connector; reseat pressure along bar).  
   - Success metric: `/sys/class/power_supply/dc/present` → **1** and non-empty `voltage_now` while Dock may become true.  
   - User already asserts keyboard USB + contact sides OK → do **not** chase “charge the pack.”

2. **Charger present-path control retest (after or with #1)**  
   - Set up **wireless adb**, unplug USB-C once, reseat keyboard, re-read `dc/present` + `kb_status`.  
   - Purpose: electrical control only; code review says USB does not soft-mask DCIN_PLUGIN.

3. **MCU protocol / resume only after present is healthy**  
   - Once DCIN presents, check whether `online` stays 1 without GPIO games.  
   - If present=1 but online still flaps: then dig screen `kb_hid_resume` sequencing / I2C protocol — still **no** userspace GPIO hold.

4. **Kernel stick-connect (ignore bit0 / never disconnect) — NOT recommended as primary long-term fix**  
   - Would paper over missing POGO power, fight real undock, needs new boot image flash risk, and prior GPIO-forced “connected” still did not prove sustained input without brick risk.  
   - Keep Force REK #45; only consider a connect-hold patch if hardware DCIN is proven good and MCU still clears bit0 spuriously — **parent OK required**.

5. **Explicitly out of scope / forbidden**  
   - Force-pull / hold `mcu_resume` (bootloop history)  
   - Remount `/vendor`, unpaired VINTF, verity/vbmeta disable  
   - Advising keyboard charging  
   - Claiming hardware success without sustained typed input

## 5) Rollback / left state
- `5-0060/power/control` = **auto**
- `tinnokeyboard` = **running** (restarted after temp stop)
- No GPIO writes this session
- No Magisk/boot changes
- Artifacts: `_online_present_live_*.txt`, `_online_present_pm_*.txt`, `_online_present_resume_*.txt`, `_online_present_tinno_*.txt` beside this report

## Verdict for parent → user
- **Best long-term:** fix tablet-side POGO **DCIN present** (electrical), then confirm MCU `online` stays up; software tinno path is already OK.
- **Why broken now:** post-ColorOS16 recovery restored HAL/VINTF, but **DCIN never asserts** and MCU only flickers online on ephemeral wake — not a `kb_batt_level` gate and not fixed by kernel stick-connect.
- **Kernel stick-connect:** reject as primary stable fix.
- hardware_success_claimed=false