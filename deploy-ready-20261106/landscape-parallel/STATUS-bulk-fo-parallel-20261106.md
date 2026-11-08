# STATUS — Bulk native FO + parallel product adaptation (2026-11-06)

**Device:** TB371FC ColorOS16 Qin `HA1W0JA3` (machineId `0bc7a3ae-6c23-4ea4-bc02-c2f0075b312d`)  
**Time:** 2026-11-06 ~22:05 Asia/Hong_Kong (UTC+8)  
**hardware_success_claimed:** false  

## KEEP (untouched this pass)
| Item | Live |
|------|------|
| SF T2 | mWorkDuration=6.94 / mReadyDuration=8.50 |
| Refresh | activeMode 144 Hz; `appSwitchBoostType=2` in `/my_product/etc/refresh_rate_config.xml` |
| Douyin+QQ FO | retained status=1 rao:true (now part of bulk table) |
| pen / luna path B / interconnect | not touched |
| Magisk / OEM-identity / ART/GC/freq/whitelist | not used |

## Classification
| Tag | Meaning |
|-----|---------|
| **system/product policy** | `/my_product/etc/fantasy/*.xml` remount bake |
| **interim data patch** | `fantasywindow.db` under exsystemservice (cloud may rewrite; product XML is durable seed) |
| **MATERIALS-BLOCKED** | FlexibleWindowUI APK same as donor 2.0.0 — settings shell stays thin |
| **rejected glue** | Magisk per-app orientation / identity spoof / magic-as-primary-landscape |

---

## 1) Landscape — bulk native FullOrientation (PRIMARY)

### Inventory (pre → post)
| Metric | Pre (live qq-fo bake) | Post (bulk-v1) |
|--------|----------------------|----------------|
| FO XML entries | 628 | 635 (+7 installed gaps) |
| FO status=1 | 476 | **630** |
| FO status=2 (PAD/trap) | 46 | **0** |
| FO status=0 | 106 | **5** (bank/payment deny) |
| Body policy | mixed traps / alwaysFullOrientActivities | **rao:true** simple (Douyin/QQ style) |

**Deny kept FO=0:** `cmb.pb`, `com.android.bankabc`, `com.ebank.creditcard`, `com.hexin.plat.android`, `com.icbc`.  

**Added FO status=1 (were missing):**  
`com.heytap.yoli`, `com.heytap.music`, `com.heytap.reader`, `com.heytap.browser`, `com.coloros.video`, `com.coloros.gallery3d`, `andes.oplus.documentsreader`.

**Transform stats:** status2→1: 45; status0→1: 103; trap simplified on status1: 2; added: 7.

### Bake paths (durable product)
| File | MD5 |
|------|-----|
| `/my_product/etc/fantasy/sys_full_orientation_managed.xml` | `1986e9bec618ed4ea2eaee78fff9e5ce` |
| Pre backup on device | `/data/local/tmp/sys_full_orientation_managed.pre-bulk-20261106-220324.xml` |
| Deploy tree | `D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\product-fo-bulk-20261106\` |

### Runtime DB sync (interim)
| Item | Value |
|------|-------|
| DB path | `/data/user_de/0/com.oplus.exsystemservice/databases/fantasywindow.db` |
| FO status counts | status0=5, status1=630 |
| WeChat FO | status=1, `{"rao":"true","rotate_cam":"false"}` |
| QQ/Douyin magic | kept status=2 + excludeDevice PAD (FO wins; magic not primary land) |

### Sample verify (native FO, not magic)
| App | Evidence |
|-----|----------|
| WeChat `com.tencent.mm` | mode=fullscreen, **land**, bounds 2944×1840, `mIsFullOrientation=true`, `OplusFullOrientationAppConfig{mStatus=1}` |
| QQ | FO status=1 live; magic=2 |
| Douyin | `mIsFullOrientation=true`, FO status=1 |
| Browser `com.heytap.browser` | `mIsFullOrientation=true`, FO status=1 |
| Yoli / Gallery / Music | FO rows inserted status=1 |

Artifacts: `product-fo-bulk-20261106/verify-sample.txt`

### Scripts
- Apply: `product-fo-bulk-20261106\apply-bulk.cmd` (product remount + DB)
- Revert product: `product-fo-bulk-20261106\revert-bulk.cmd` (+ restore `fantasywindow.pre-bulk.db` via same DB deploy pattern if needed)

---

## 2) Parallel 平行视界 adaptation (product/DB only)

### What changed (allowed without new UI APK)
| Change | Class | Detail |
|--------|-------|--------|
| Fantasy product XML +7 magic entries for installed gaps (yoli/music/reader/browser/video/gallery/documentsreader) | system/product | MD5 live `0de66d2fc04bc2e34cb4338f4a297ac1` |
| Magic allowlist richness | already present | ~2887 status=1 magicwindow rows in product/DB — **not** the thin settings UI |
| WeChat magic | kept status=1 | dual-pane parallel eligible |
| QQ/Douyin magic | kept status=2 | so native FO landscape is primary |

### MATERIALS-BLOCKED (once; do not re-ask piecemeal)
Settings shell `OplusFlexibleWindowUI` **2.0.0** hash matches donor — UI remains float-tutorial thin.  
Need old R94 `OplusFlexibleWindowUI.apk` with **different** hash than live `01450E66…` (see `MATERIALS-REQUEST-parallel-ui-20261106.md`).  
**Cannot** restore old rich parallel console from product XML/DB alone.

---

## 3) Rollback
1. `product-fo-bulk-20261106\revert-bulk.cmd` → restores pre-bulk FO+fantasy XMLs (MD5 FO `5848af15…`).  
2. DB: push `fantasywindow.pre-bulk.db` and run prior `apply-bulk-db.sh` pattern against that file.  
3. KEEP refresh/T2/boost untouched by this rollback.

## 4) Out of scope / rejected
- Magic window as primary landscape substitute  
- OEM identity spoof for QQ phone login  
- Magisk per-app orientation modules  
- FlexibleWindowUI APK replace without MATERIALS  

## 5) User action
Rotate device / open WeChat, QQ, Douyin, Browser, Yoli — expect **fullscreen native land** (not side-by-side magic fake).  
Parallel list in Settings UI will still look thin until MATERIALS APK arrives; backend allowlists are expanded.
