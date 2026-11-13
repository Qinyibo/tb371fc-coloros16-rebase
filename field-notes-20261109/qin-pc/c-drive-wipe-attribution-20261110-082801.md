# C: drive / profile hollow — forensic attribution

**Machine:** Qin (Windows) — `C:\Users\Administrator` (SID `S-1-5-21-3975006397-4113282330-3633100300-500`)  
**Report written:** 2026-11-10 ~08:28 Asia/Hong_Kong  
**Scope:** Attribution + recovery assessment only (no destructive restore executed)

Also on Qin Desktop:
- Recovery interim: `C:\Users\Administrator\Desktop\c-wipe-recovery-interim-20261110-082444.md`
- Box copy of interim: `/workspace/boot-diag-out/c-wipe-recovery-interim-ASAP.md`

---

## Executive answers (required)

### WHO?
**Unknown — no process/user/agent left a deletable audit trail for the Nov 9 hollow.**

Ruled out / not the deleter (with evidence):
| Suspect | Verdict | Evidence |
|---------|---------|----------|
| **NetGuard_Logon / NetGuard_Timer** | **Not deleter** | Task XML only runs `wscript.exe C:\Users\Administrator\Scripts\net-guard.vbs`. No delete actions. Tasks **Disabled** by Tibo after popup; Scripts only has README noting missing VBS. |
| **Storage Sense / SilentCleanup** | **Not the Nov 9 Documents wipe** | Enabled (recycle+Downloads age cleanup). **LastTrigger = 2026-11-08 10:25:34** Asia/Hong_Kong (day *before*). Does not delete the Documents folder tree by design. No StorageSense Operational log channel on this PC. |
| **This bot (Tibo) tablet / Force REK / adb work** | **No** | Work artifacts under `E:\youxikaifa\work\` (today-20261109 boot-diag, etc.). `.grokbot\local-exec-daemon.log` shows connection watches only — **no** `Remove-Item` / profile deletes. Agent-tools dump references tablet `official-wipe` **device** logs on E:, not C: profile. |
| **User Profile Service reset** | **No full profile recreate** | `NTUSER.DAT` / `AppData` create dates from **2026-03-29**; UPS log shows normal logon/logoff only. Documents folder recreated at **2026-11-10 08:13** login (OPPO 互联), not a whole new profile. |
| **OneDrive reset** | **N/A** | OneDrive folder/process absent. |

Unproven possibilities (no Security 4660/4663 auditing; no PSReadLine history; Prefetch stale/cleared since ~2026-07):
- Manual Explorer / **360FileBrowser64** delete (360 crashed repeatedly **20:21** Nov 9 — *after* hollow already visible at **20:13**; 360 processes still running; **not proven** as the actor).
- Another agent (Codex / WorkBuddy / dsh / qclaw) without retained delete commands in surviving logs (grep of Nov 9 agent text files found no actionable `Remove-Item` on profile known folders; Codex plugin docs false-positive on the word “documents”).

### HOW?
**Permanent removal bypassing Recycle Bin**, then hollow folders recreated later by apps/login.

Mechanism indicators:
1. **Zero** C: `$Recycle.Bin` `$I` metadata files with LastWriteTime in **2026-11-09 00:00 – 2026-11-10 08:30**.
2. Newest recycle `$I` entries are **2026-11-08 ~12:23** (TRAE / Codex / `.workbuddy` junk under AppData — unrelated to Documents tree wipe).
3. Consistent with `Shift+Delete`, `Remove-Item -Recurse -Force`, `rd /s /q`, or a cleaner that skips the bin — **not** a normal Explorer “Delete → Recycle Bin” of Documents.

Not: whole-disk format, Sysprep, or C: wipe (OS / Program Files / ~231 GB used intact).

### WHEN? (Asia/Hong_Kong)
| Time | Event |
|------|--------|
| **≤ 2026-11-09 ~20:13** | Profile known folders already gone (Documents/Videos/Music/Favorites/etc.). |
| **2026-11-09 20:13:09** | `Downloads` **recreated**; `Downloads\Programs\Grok_Bot_0.79.3_Setup.exe` appears. |
| **20:14** | `Grok Bot.lnk`, `Brave.lnk` on Desktop; Shell AppResolver registers Grok Bot / Brave. |
| **20:18** | `Scripts` recreated; Tibo disables NetGuard, writes README; PowerShell Start Menu shortcut restored. |
| **20:21** | `Pictures` recreated (desktop.ini); **360FileBrowser64** crash storm. |
| **2026-11-10 08:13** | User logon; empty `Documents` recreated with `OPPO 互联` only. |

Best estimate for the destructive act: **sometime on 2026-11-09 before ~20:13 Asia/Hong_Kong** (possibly earlier that day; no `$I`/audit pin).

### WHAT removed vs survived?
**Survived (not a full C: wipe):**
- Windows, Program Files, ProgramData, ~231 GB used / ~246 GB free on C:
- `AppData` (Roaming/Local/LocalLow present)
- `Desktop` folder (create 2026-07-04) + some items
- Agent dirs: `.codex`, `.qclaw`, `.dsh`, `.grokbot`, `WorkBuddy`
- `NTUSER.DAT` (profile hive)
- **`E:\youxikaifa\work\` intact** (247 children spot-check OK)

**Missing or hollow:**
- Missing folders: **Videos, Music, Favorites, Links, Searches, Contacts, Saved Games, OneDrive, 3D Objects**
- Recreated empty/near-empty: **Documents** (only OPPO 互联), **Downloads** (Programs + later installer), **Pictures** (UbisoftConnect + desktop.ini), **Scripts** (README only; `net-guard.vbs` gone)

**Not redirected:** User Shell Folders still point to `C:\Users\Administrator\...`.  
**`D:\Documents`:** old (2024) game/app data tree — **not** a live redirect of the wiped profile Documents; registry `Personal` still C:.

### Did THIS bot’s tablet / Force REK / adb work cause it?
**NO.**

Proof summary:
- Tablet flash/wipe logs and tooling live under **`E:\youxikaifa\work\today-20261109\...`** (device userdata wipe ≠ PC profile).
- Grokbot local-exec log: gateway/watch noise only; no profile delete commands.
- NetGuard disable **after** discovery of missing VBS created `Scripts\README.txt` — restorative, not destructive.
- No evidence linking adb/`android-sdk` host activity to deleting `C:\Users\Administrator\Documents`.

### Recovery options (not executed)
| Path | Outlook |
|------|---------|
| Recycle Bin restore | **No** for Nov 9 hollow (`$I` Nov9–Nov10am = 0) |
| Previous Versions / VSS | **No** (ShadowCopy count=0; vssadmin empty) |
| OneDrive recycle | **No** (not present) |
| `D:\Documents` | Unrelated game saves — optional browse, not the missing C: Documents |
| `E:\youxikaifa\work\` | **Intact** — primary work data OK |
| Undelete (Recuva/R-Studio/PhotoRec) | Uncertain; **stop heavy writes to C:** first |
| Do **not** | Empty Recycle Bin, Disk Cleanup, Storage Sense, fill C: |

---

## Evidence appendix (selected)

### Disk / inventory
- C: UsedGB≈230.7 FreeGB≈246 — OS intact.
- Shell folders: Personal/Desktop/Downloads → under `C:\Users\Administrator\...` (no off-disk redirect).

### Recycle Bin
- C: ~92,421 `$I` files; D: ~25,101; E: 49.
- Nov 9–Nov 10 08:30 `$I` count: **0**.
- Nov 8 hits: largely `AppData\Roaming\TRAE SOLO CN\...` and Codex session deletions.

### Scheduled tasks
- `\NetGuard_Logon`, `\NetGuard_Timer`: Disabled; Exec `wscript` + `net-guard.vbs` only.
- `\Microsoft\Windows\DiskCleanup\SilentCleanup`: Ready (`cleanmgr /autocleanstoragesense`).
- `\Microsoft\Windows\DiskFootprint\StorageSense`: Ready.

### Storage Sense registry
- Enable=1; Temp=1; Recycle=1; Downloads=1; RecycleDays=30; DlDays=30.
- LastTrigger **2026-11-08 10:25:34**; LastFailure **10:25:47**.

### Event logs
- Security 4660/4663 Nov 9 afternoon–evening: **none** (auditing not enabled).
- UPS: normal session logon/logoff; Documents recreate aligns with **2026-11-10 08:13** logon.
- Application ~20:21 Nov 9: repeated **360FileBrowser64.exe** APPCRASH.
- Shell-Core ~20:13–20:18: Grok Bot / Brave / PowerShell shortcut registration (install/UI), not deletes.

### Agent traces
- `.grokbot`: daemon connectivity; settings.json ~20:14:49 Nov 9.
- Scripts README: “net-guard.vbs was missing; NetGuard_* disabled 2026-11-09 by Tibo.”
- No PSReadLine history file present.
- Prefetch for cmd/powershell/360 mostly stuck at **2026-07** timestamps (limited usefulness).

### Folder create times (critical)
| Path | Create (Asia/Hong_Kong) |
|------|-------------------------|
| Desktop | 2026-07-04 (survived) |
| Downloads | **2026-11-09 20:13** (recreated) |
| Scripts | **2026-11-09 20:18** |
| Pictures | **2026-11-09 20:21** |
| Documents | **2026-11-10 08:13** |
| AppData | 2026-03-29 (survived) |

---

## Confidence

- **Recovery built-in: high confidence NO.**
- **Not whole C: wipe: high.**
- **NetGuard / StorageSense-as-Documents-wiper / this-bot-tablet-work: high confidence NOT.**
- **Exact WHO process name: low** — no object-access auditing, no recycle metadata for the act, no PS history.

## Recommended next steps (for user / parent; not done here)
1. Treat Recycle Bin / Previous Versions as exhausted for this incident.
2. If Documents content was critical and not on E:/D: backups: consider offline undelete ASAP; avoid writing to C:.
3. Optionally inspect 360 Safe “清理/粉碎” history UI manually (no API dug here).
4. Enable file-delete auditing if future attribution matters.
5. Keep work on **E:\youxikaifa\work\**; do not rely on hollow C: profile folders.

