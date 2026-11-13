# D: backup inventory for wiped C:\Users\Administrator

- Machine: Qin (`d034a1ca-7f3e-4320-ba7e-4a4db4e6fc6b`)
- Scanned: 2026-11-10 ~08:44–08:48 Asia/Shanghai (UTC+8)
- Scope: inventory only — **nothing restored**, recycle bin **not** emptied, nothing deleted
- Target loss: C:\Users\Administrator profile hollowed before **2026-11-09 ~20:13** Asia/Shanghai

## Verdict

**PARTIAL** — not a full profile backup of the Nov-9 wipe.

| Usable for Nov-9 Documents/Scripts/AppData wipe? | Result |
|---|---|
| Full profile / Documents / Scripts / AppData mirror | **NO** |
| Desktop (pre-2026-11-08 cleanup snapshot) | **YES (in D: Recycle Bin)** |
| Browser / chats / fonts / old desktop archive | **YES (partial, older or other scope)** |
| VSS / Previous Versions / File History | **NO (0 shadows)** |

## Best candidate(s)

### 1) BEST — `D:\C_Cleanup_Backup_20261108` (deleted, still in Recycle Bin)

- **Live path:** does **not** exist (`D:\C_Cleanup_Backup_20261108` gone)
- **Recoverable from:** `D:\$RECYCLE.BIN\…` — **25,101** `$I`/`$R` pairs, **~$41.9 GB** declared, **all `$R` present**
- **Deleted:** 2026-11-08 **12:05:28 – 12:29:02** Asia/Shanghai
- **What it is:** a **C-drive cleanup staging tree** from Nov 8 (A* = caches/temp/updaters; B* = moved user-ish content), **not** a full `C:\Users\Administrator` clone, and **not** dated after the Nov-9 wipe
- **Useful subset for profile-adjacent restore:**
  - `B1_desktop_backup` — **~10.3 GB / 3,739 items / 150 top-level names** — Desktop dump (installers, PSD/AI/PDF, `Desktop.rar` 73.5MB, `erp`, `gjx`, PE tools, shooting clips, etc.)
  - `B4_trae` — ~1.1 GB (TRAE ModularData)
  - `B4_minimax_sessions` — ~894 MB
  - `B2_claude_vm_old` — ~10.4 GB (Claude VM rootfs; not Documents)
  - `A1_Temp` / `A2_pipcache` / `A3_NV_ota` / `A5_NV_DXCache` / `A6_*` — mostly **junk/cache**, low value for “lost Documents”
- **Does NOT cover:** `C:\Users\Administrator\Documents`, `Scripts`, general `AppData`, `Videos`/`Music`/`Favorites` from the Nov-9 event
- **Recycle note:** **0** `$I` paths under `C:\Users\Administrator\…` on D: recycle; Nov-9 wipe did **not** land there

### 2) Live on D: (secondary / older — not Nov-9 profile mirror)

| Path | ~Size / date | Covers | Notes |
|---|---|---|---|
| `D:\Documents` | ~8.6 GB; newest WeChat bits 2026-11-09 22:22 | WeChat/`xwechat_files`, games, misc | **Not** shell-folder redirect; HKCU Personal still `C:\Users\Administrator\Documents` |
| `D:\下载\桌面` | ~18.6 GB; newest ~2024-05 | Old Desktop archive | Too old for Nov-9 loss |
| `D:\ChromeBackup_20260812` | ~4.2 GB; 2026-08-12 | Chrome User Data + DPAPI note | Browser only |
| `D:\Codex_Recovered_20261108` | ~1.4 GB; 2026-11-08 | Codex chat JSONL/MD + sqlite snapshot | Mentions C: paths in titles; **not** the files |
| `D:\CodexBackups` | ~70 GB; Oct 2026 | RG35XXPRO device images | Unrelated to Windows profile |
| `D:\字体备份` | many fonts; 2025-02 | Fonts only | |
| `D:\AppData\Roaming` | empty Adobe stub; 2024-07 | Useless | |
| `D:\PSAutoRecover\Administrator` | 2× ~1.1–1.3 GB PSB; 2026-11-07 | Specific Photoshop recovers | |
| `D:\ZhihuaCanvasBackup` | canvas objects/runs | Project-specific | |
| `D:\移动云盘同步盘` | empty | — | |
| `D:\123pan` | downloads only | — | |
| `D:\BaiduNetdiskDownload` | games/courses/media | Not a profile tree | |

### 3) Missing backup roots (checked)

No live: `D:\backup*`, `D:\Backup*`, `D:\备份`, `D:\Users`, `D:\Administrator`, `D:\Desktop`, `D:\Scripts`, `D:\FileHistory`, `D:\WindowsImageBackup`, OneDrive/Google Drive/iCloud/Syncthing profile mirrors, Macrium/Acronis/EaseUS/AOMEI image folders.

### 4) Volume / VSS / redirects

- **D:** NTFS label `学习资料`, size ~16.4 TB, free ~4.3 TB
- **vssadmin / Win32_ShadowCopy:** **no shadow copies** (C and D)
- **Shell folders:** Desktop/Documents/Downloads/Music/Pictures/Videos all still under `C:\Users\Administrator\…` (not redirected to D:)

## Recommended restore steps (for parent — DO NOT RUN yet)

1. **Do not empty** Recycle Bin on D: (or C:). Do not run Disk Cleanup / Storage Sense until a restore decision.
2. **Staging restore only** of the useful Recycle subset:
   - Create e.g. `D:\restored_from_recycle\C_Cleanup_Backup_20261108\`
   - Restore **only** `B1_desktop_backup` (optional: `B4_trae`, `B4_minimax_sessions`) from Recycle UI or a scripted `$I`→original-name copy into staging
   - **Do not** restore A* cache buckets unless specifically needed
   - **Do not** overwrite live `C:\Users\Administrator\Desktop` blindly — diff against staging first
3. Inspect `B1_desktop_backup\Desktop.rar` (73.5 MB) in staging after restore — may be a packed Desktop snapshot.
4. Treat `D:\Documents` / `D:\下载\桌面` as **extra sources to cherry-pick**, not as the Nov-9 Documents recovery.
5. For **Nov-9 Documents/Scripts/AppData** specifically: D: inventory does **not** show a usable full backup. Remaining options are outside this ask (C: undelete with DiskGenius already on `D:\DiskGenius.exe`, cloud accounts, E: work copies). Prefer stop-writes on C: before any undelete pass.
6. After user confirms what they want back, restore file-by-file from staging → final locations.

## Scan artifacts (helper scripts left on Desktop)

- `C:\Users\Administrator\Desktop\d_backup_scan1.py`
- `C:\Users\Administrator\Desktop\d_backup_scan2.py`
- `C:\Users\Administrator\Desktop\d_recycle_scan.py`
- `C:\Users\Administrator\Desktop\d_cleanup_backup_inventory.py`
- `C:\Users\Administrator\Desktop\d_b1_and_manifest.py`

Safe to delete those scripts later; they did not modify D: data.
