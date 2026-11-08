import re
from pathlib import Path
p=Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\pscanvas-ui.xml")
if not p.exists():
    print("no ui xml"); raise SystemExit
t=p.read_text(encoding="utf-8",errors="replace")
texts=re.findall(r'text="([^"]+)"', t)
texts=[x for x in texts if x.strip()]
print("UI texts count", len(texts))
for x in texts[:80]:
    print("-", x)
# unique
seen=[]; 
for x in texts:
    if x not in seen: seen.append(x)
Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\pscanvas-ui-texts.txt").write_text("\n".join(seen),encoding="utf-8")
print("unique", len(seen))
