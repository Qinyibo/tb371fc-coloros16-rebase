from pathlib import Path
text=Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\activities-native-v2-settled.txt").read_text(encoding="utf-8",errors="replace")
lines=text.splitlines()
# find aweme task block
out=[]
in_aweme=False
for i,line in enumerate(lines):
    if "A=10336:com.ss.android.ugc.aweme" in line and "Task{" in line:
        in_aweme=True
    if in_aweme:
        if any(k in line for k in ("Task{","ActivityRecord","mode=","CurrentConfiguration","mOverrideConfig","requestedOrientation","overrideOrientation","mBounds=","config info","mActivityComponent","Hist")):
            out.append(line.strip()[:350])
        if line.strip().startswith("* Task{") and "aweme" not in line and len(out)>5:
            break
Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\aweme-native-v2-settled.txt").write_text("\n".join(out),encoding="utf-8")
print("\n".join(out[:50]))
# classify
blob="\n".join(out)
print("==== CLASSIFY ====")
print("magic" if "oplus-magic-windows" in blob else "not-magic")
print("fullscreen-mode" if "mode=fullscreen" in blob else "other-mode")
print("LAND" if " widecg land " in blob or "wideColorGamut land" in blob or " widecg land " in blob else "check-orient")
# more precise
import re
orients=re.findall(r"widecg (land|port) ", blob)
print("orients found:", orients[:20])
print("bounds snippets:", re.findall(r"mBounds=Rect\([^)]+\)", blob)[:6])
