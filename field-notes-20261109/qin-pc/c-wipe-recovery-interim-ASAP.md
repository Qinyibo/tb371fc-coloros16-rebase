# C: profile data — recovery interim (ASAP)

**When:** 2026-11-10 08:25 Asia/Hong_Kong  
**PC:** Qin `C:\Users\Administrator`  
**Also on Qin Desktop:** `C:\Users\Administrator\Desktop\c-wipe-recovery-interim-20261110-082444.md`

## Can wiped profile data be recovered?

### Verdict: **NO via Recycle Bin / Previous Versions** (built-in)

| Source | Result |
|--------|--------|
| **Recycle Bin** | **No.** C: `$I` entries with LastWriteTime on **2026-11-09 → 2026-11-10 08:30 = 0**. Newest recycle metadata is **2026-11-08 ~12:23**. Nov 9 hollow **did not land in Recycle Bin** (permanent delete / `Remove-Item` / `rd`, or non-recycle mechanism). Bin still has older TRAE/Codex/AppData junk — not the missing Documents tree. |
| **VSS / Previous Versions** | **No.** ShadowCopy count=0; `vssadmin` shadows & shadowstorage empty. |
| **OneDrive** | **No.** Folder absent; process not running. |
| **Redirects** | **None.** Documents/Desktop/Downloads still under `C:\Users\Administrator\...`. |

## Current hollow state (not whole-disk wipe)

- C: ~231 GB used / ~246 GB free — OS intact.
- Documents: recreated **2026-11-10 08:13** with only `OPPO 互联`.
- Desktop / Downloads / Pictures / Scripts / AppData: present (Scripts = README only; `net-guard.vbs` missing).
- Missing: Videos, Music, Favorites, Links, Searches, Contacts, Saved Games, OneDrive, 3D Objects.

## What user can still try

1. Recycle Bin manual browse — **low hope** for Nov 9 Documents.
2. Previous Versions — **expect empty**.
3. Optional undelete (Recuva etc.) on C: — uncertain; **stop heavy writes to C:** first.
4. Confirm **E:\youxikaifa\work\** still intact (was OK Nov 9 evening).

**Do not** empty Recycle Bin / Disk Cleanup / Storage Sense / fill C:.

Attribution (WHO/HOW) still running — NetGuard only launches VBS (no delete); Storage Sense enabled but does not delete Documents folder by design.
