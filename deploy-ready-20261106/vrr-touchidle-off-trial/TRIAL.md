# VRR TouchIdle OFF Magisk trial

**时间:** 2026-11-06 Asia/Hong_Kong  
**hardware_success_claimed=false**  
**模块:** `tb371fc_vrr_touchidle_off`（**已装机 ENABLED**）  
**zip:** `D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\vrr-touchidle-off-trial\tb371fc_vrr_touchidle_off-trial.zip`

## 变更（仅 product JSON bind）
`/my_product/etc/oplus_vrr_config.json` TouchIdle 块：

| 字段 | stock | trial |
|------|-------|-------|
| touch_idle | true | **false** |
| hw_enable | true | **false** |
| sw_enable | true | **false** |
| adfr_enable | false | false |
| sw_whitelist_3rd | Douyin等→[30] | **{}** |

未改 FRTC / refresh / dynframe。禁止 jar / ART / 按 app rateId 胶水。

## MD5
| | MD5 |
|--|-----|
| stock | `e21e0be326d37a0f431a91fef4d2dbc0` |
| patched | `495ad3fc5ae9b4abbced79df54eb64db` |
| zip（POSIX 路径 + LF script） | 见文件 hash；当前 zip 用 Python zipfile 打包 |

## 开机验收（已通过 2026-11-06 15:02 Asia/Hong_Kong）
- bind MD5=`495ad3fc…`
- `TouchIdleBean{mEnable=false, mHwEnable=false, mSwEnable=false}`
- PickRate 仍 144；Preferred `[4,4,2,4]`；dynframe 仍 disable（`910955b1…`）
- 顶栏 `TouchIdle switch: true …` 为能力摘要，以 Bean 为准

## 暖打断 A-on 自测目录
`follow-finger-20261106/vrr-touchidle-A-on-*`（am start + adb swipe；**主观真指未做**，不可宣称跟手成功）

## 回滚
```
adb shell su -c 'touch /data/adb/modules/tb371fc_vrr_touchidle_off/disable'
adb reboot
# md5 -> e21e0be326d37a0f431a91fef4d2dbc0
```

## 注意
首版 zip 若用 .NET ZipFile 会带反斜杠路径导致 bind 失败；务必用本目录当前 zip（forward slash + Unix LF `post-fs-data.sh`）。
