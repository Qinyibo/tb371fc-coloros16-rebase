from pathlib import Path
text = Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\activities-after-native.txt").read_text(encoding="utf-8", errors="replace")
out=[]
capture=False
for line in text.splitlines():
    if "com.ss.android.ugc.aweme" in line and ("Task{" in line or "ActivityRecord" in line or "Hist" in line):
        capture=True
    if capture:
        keys=("Task{","TaskFragment","ActivityRecord","mode=","mWindowingMode","requestedOrientation","CurrentConfiguration","mOverrideConfig","mBounds","mAppBounds","mDisplayRotation","mRotation","port ","land ","oplus-magic","fullscreen")
        if any(k in line for k in keys) or line.strip().startswith("*"):
            out.append(line.rstrip()[:300])
        if "requestedOrientation=" in line and "aweme" in "".join(out[-20:]):
            # keep a bit more then stop after orientation of aweme
            pass
Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\aweme-native-evidence.txt").write_text("\n".join(out[:120]), encoding="utf-8")
print("\n".join(out[:80]))
