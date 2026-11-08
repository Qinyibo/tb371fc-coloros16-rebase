# STATUS — QQ parallel/magic fix (2026-11-06 ~22:35 HKT)

**Device:** TB371FC ColorOS16 Qin HA1W0JA3  
**Package:** `com.tencent.mobileqq`  
**hardware_success_claimed:** false  

**KEEP verified:** SF T2 6.94/8.50; `appSwitchBoostType=2`; FWUI SHA `19D32858…`; FO bulk for non-magic apps untouched; no OEM spoof.

---

## Root cause

| | WeChat (worked after toggle) | QQ (before) |
|--|--|--|
| magic `config` | rich ~8275B: `activityPairs` LauncherUI→*, `defSwitch=magic`, UX… | **only `{"mode":"1"}`** (12B) |
| `custom_config_body` | `scaleWindow=-1`, UX isDraggable | Activities/* camera only — **no activityPairs / scaleWindow** |
| FO | status=2 | status=2 (already demoted) |
| Product XML QQ row | — | same thin body; **TIM** had the real SplashActivity pairs |

Toggle alone could not invent pairing rules for QQ. WeChat already had them baked.

## Fix (product + runtime)

Applied TIM-pattern SplashActivity pairs + WeChat-style `defSwitch=magic` / `scaleWindow=-1` / `UX.isDraggable`:

```json
{
  "force_custom_pw_mode":"true","mode":"1","defSwitch":"magic",
  "activityPairs":[{"from":"com.tencent.mobileqq.activity.SplashActivity","to":"*"}],
  "Activities":[{"name":"*","reverseCameraRotation":"10","reverseCameraRotationFront":"9"}],
  "transActivities":["com.tencent.mobileqq.activity.LoginActivity"],
  "noRelaunchOnResize":"true","adjustDisplayRotation":"0","blockSensor":"true",
  "scaleWindow":"-1","changeToFullscreen":"true",
  "UX":{"isDraggable":"true"}
}
```

| Layer | Path | Result |
|-------|------|--------|
| Product | `/my_product/etc/fantasy/sys_fantasy_window_managed.xml` | MD5 `f6043030…` (pre bak `/data/local/tmp/sys_fantasy_window_managed.pre-qqfix-20261106-223419.xml`) |
| Runtime DB | `fantasywindow.db` magic row | config len 453; FO still status=2 |

Scripts: `qq-parallel-fix-20261106\apply-qq-fix.cmd` / `rollback-qq-db.cmd`

## Verify

After force-stop + relaunch (landscape):

- Task **mode=`oplus-magic-windows`**
- **TaskFragment** present (not FO fullscreen land)
- Activity: `SplashActivity`

Same as WeChat: **open a chat/session** to see left–right dual pane (`activityPairs` Splash→*). Single Splash page may still look one-pane until a related activity opens.

## User check

1. Kill QQ from recents, reopen landscape.  
2. Confirm parallel switch ON in 平行视窗.  
3. Tap a conversation — expect dual layout.  
4. If stale, toggle QQ switch once (Settings writes custom_mode) then reopen.

## Classification

| Tag | Meaning |
|-----|---------|
| system/product policy | fantasy XML remount bake |
| interim runtime | DB sync via exsystemservice PID `su -t` |
| not glue | no Magisk bind / identity spoof / FO=1 override |