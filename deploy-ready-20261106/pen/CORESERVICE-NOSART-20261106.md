# CoreService no-start diagnosis · Pen V4 on e088 · 2026-11-06

`hardware_success_claimed=false`  
**No re-flash performed.** Read-only adb/su probe + design-source cross-check.

Written: 2026-11-06 Asia/Hong_Kong (box/Qin local).

## Verdict (one line)

**Absence of a physical CTN730 alone explains no CoreService PID.** V4 software gate is waiting on pen attach (`attached=1` + valid MAC via system `CTN730_STATE`). This is **expected vs V3**, not a disabled-component / missing-permission regression. No safe offline software enable/prop fix; next step is real-pen attach acceptance.

## Live facts (post V4 flash, super `7b1c6736…`)

| Check | Result |
| --- | --- |
| `services.jar` SHA-256 | `6a3caff3686b55ec58e492e8dc69090efe7c269e42327b454e0efe6308a8b490` (V4) |
| `IPeManager.apk` SHA-256 | `bfdae2e161774767a2c0dc94598fb78cdfa0e8063a00e7d6a459340311a956f2` (V4) |
| Package | `com.oplus.ipemanager` 16.13.0 / 16130000, `appId=10118`, User0 `enabled=0` (default), `stopped=false`, `hidden=false` |
| sharedUserId / SYSTEM_UID | **No** sharedUserId; runs as appId 10118 (not uid 1000) |
| CoreService | Manifest-registered; resolver shows filter + `permission=com.oplus.permission.safe.IOT` |
| BluetoothStatusReceiver | Registered for `android.bluetooth.device.action.ACL_CONNECTED`; `cmd package query-receivers` returns it |
| `dumpsys activity services com.oplus.ipemanager` | `(nothing)` — **no ServiceRecord**, no PID |
| `pidof` IPe / `:ble` | empty |
| Install perms | `com.oplus.permission.safe.IOT` **granted=true**; BT CONNECT/SCAN granted-by-default |
| BT adapter | ON; **Bonded devices: 0** |
| Refresh XML MD5 | `35db38f8c85758c372546c707513642c` (intact) |
| SELinux | Enforcing |
| Diagnostic Settings.Global | `tb371fc_pen_system_bridge_ready=1`, `tb371fc_pen_input_bridge_ready=1`, `tb371fc_pen_ctn_bridge_ready=1` |
| CTN730 sysfs (`su`) | `attached=0`, `mac=00:00:00:00:00:00`, `level=-1`, `charge_state=Unknown`, `status=detecting`, `enable=1`, `version=1041` |
| Input | `NVTCapacitivePen` present (`input/pen`, BTN_STYLUS / BTN_STYLUS2) — digitizer path ≠ BLE CoreService |
| Broadcasts | `NativePenSystem` receivers live in system_server (incl. `REQUEST_CTN730_STATE`); history shows `act=org.tb371fc.pen.CTN730_STATE … cmp=…BluetoothStatusReceiver` delivered |

Probe dump dir: `deploy-ready-20261106/pen/nosart-probe-20261106-171801/`

## V4 start path (from sources)

1. `PhoneWindowManager.systemReady` → `NativePenSystem.start` (services.jar) — **confirmed live** by three `*_bridge_ready=1` marks + registered system receivers.
2. CTN730 UEvent / sysfs snapshot → `publishHardware` → broadcast `org.tb371fc.pen.CTN730_STATE` to `BluetoothStatusReceiver` as SYSTEM_UID with `BLUETOOTH_PRIVILEGED` + share-identity.
3. Patched `BluetoothStatusReceiver.onReceive` → `NativePenLifecycle.hardware()`:
   - Requires action `CTN730_STATE` and `getSentFromUid()==SYSTEM_UID`.
   - `NativeHardwareState.receive`: **`attached==0` → return false (no CoreService start)**; only `attached==1` + valid MAC + `mac_is_current` proceeds to `context.startService(CoreService)`.
4. After CoreService `onCreate`, native lifecycle may reconnect **already-bonded** pens (`identity` requires `BOND_BONDED` + official name / known CTN MAC). With **0 bonded devices**, reconnect would no-op even if service were forced up.

Design docs: `DEPLOY.md` / `DEPLOY-FROM-E088.md` — “真笔 CTN730 → manifest 接收器 → SYSTEM_UID 校验 → 应用自管 CoreService”.

## Contrast with V3

| | V3 (`v3-core-start-dumpsys.txt`) | V4 (this boot) |
| --- | --- | --- |
| ServiceRecord | Present: `CoreService`, `recentCallingUid=1000` / `callingPackage: android` | **Absent** `(nothing)` |
| `app=` / PID | `app=null`, PID empty | No record at all |
| Meaning | System **attempted** start at boot; process failed to come up | System **intentionally does not** boot-start CoreService; waits for CTN attach snapshot |

So “no PID” on V4 with no pen is **not the same failure mode** as V3 `app=null`. V4 looks healthier on the gate path; hardware still unproven.

## Ranked root-cause candidates

1. **Expected — no physical CTN730 attached (PRIMARY)**  
   Evidence: `attached=0`, zero MAC, BT bonded=0, bridges ready=1, `CTN730_STATE` already delivered to receiver, CoreService start code only runs when `receive()` accepts attach=1.  
   **Explains no PID alone.**

2. **Expected companion — no bonded BLE pen**  
   Evidence: `Bonded devices: 0`. Would block native auto-GATT reconnect after a future CoreService start until bond exists. Does not by itself block the attach→startService path.

3. **Ruled out — component disabled / package stopped / missing IOT permission**  
   Evidence: User0 enabled default, not stopped; receiver resolves; `safe.IOT` granted; CoreService in Service Resolver Table.

4. **Ruled out — V4 jars / system bridge missing**  
   Evidence: APK/jar SHAs match V4 integration JSON; all three bridge Settings marks = 1; NativePenSystem broadcast filters present.

5. **Low — early-boot logcat empty for `TB371FCPen*`**  
   Buffer likely rotated (~8+ min uptime); marks + broadcast history supersede. Not treated as bridge failure.

6. **Not pursued — manual `am start-service` as “fix”**  
   Would not prove CTN path; could leave a running service without a pen and muddy hardware trial. Documented only (below). DEPLOY does not authorize this as acceptance.

## ONE next executable step

**Attach a real CTN730-compatible pen** (tablet charge/pair / detect zone until sysfs flips), then re-check — **no flash, no Magisk toggle, no component enable**:

```text
adb shell su -c 'cat /sys/class/misc/ctn730/attached; cat /sys/class/misc/ctn730/mac; cat /sys/class/misc/ctn730/level'
adb shell 'settings get global tb371fc_pen_ctn_bridge_ready'
adb shell 'dumpsys activity services com.oplus.ipemanager'
adb shell 'pidof com.oplus.ipemanager com.oplus.ipemanager:ble'
adb logcat -d -s TB371FCPen:I TB371FCPenSystem:I | tail -n 80
```

Pass gate for “software start path”: `attached=1`, non-zero MAC, non-empty CoreService ServiceRecord / PID, and ideally a `TB371FCPen` “trusted CTN730 snapshot” / service-start line.  
Then continue FLASH-RESULT pen hardware checklist (pair / battery / pressure / side button / in-app vs game). Keep `hardware_success_claimed=false` until that checklist passes.

Diagnostic-only (do **not** use as acceptance; stop with `am stopservice` if tried):

```text
adb shell am start-service -n com.oplus.ipemanager/.btadsorb.CoreService
adb shell am stopservice -n com.oplus.ipemanager/.btadsorb.CoreService
```

**Software gate statement:** waiting on pen attach for the SYSTEM_UID `CTN730_STATE` receiver path. No further offline software rebuild/enable required for this no-PID symptom.

## Comm next-priority inventory (no flash started)

`deploy-ready-20261106/comm/TRIAL.md` status:

- Offline-only trial checklist; **explicitly not offline-passable**.
- Needs real phone: pair → capability negotiate → link → tablet browse via phone data; voice/SMS separate; O+ Connect PC remote **out of scope**.
- Identities noted (commcenterd / `oplus_vnet.ko` / NAS / OplusVirtualComm / WirelessSettings path); VirtualComm APK hash ≠ v17 — regression open.
- **No new comm delta attached; do not invent “share success”.** Not safe to start a heavy comm flash from this folder alone.

## Paths

- This note: `D:/TB371FC-release/clean-rebase-20261104/deploy-ready-20261106/pen/CORESERVICE-NOSART-20261106.md`
- Flash result: `…/pen/FLASH-RESULT-E088-20261106.md`
- Deploy: `…/pen/DEPLOY-FROM-E088.md` (V3→V4 DEPLOY.md obsolete)
- V3 dumpsys: `…/handoff-to-grok-20261106/pen/v3-core-start-dumpsys.txt`
- Design: `pen-sharing-compat/system-src/org/tb371fc/pen/system/NativePenSystem.java`, `src/org/tb371fc/pen/NativePenLifecycle.java`, `NativeHardwareState.java`
- Live probe: `…/pen/nosart-probe-20261106-171801/`
- Comm: `…/comm/TRIAL.md`
