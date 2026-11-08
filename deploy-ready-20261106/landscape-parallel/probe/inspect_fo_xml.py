from pathlib import Path
import re
p=Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\sys_full_orientation_managed.stock.xml")
t=p.read_text(encoding="utf-8", errors="replace")
print("len", len(t), "head:", t[:400])
# find mobileqq and aweme blocks
for pkg in ["com.tencent.mobileqq", "com.ss.android.ugc.aweme"]:
    print("\n====", pkg)
    for m in re.finditer(re.escape(pkg), t):
        start=max(0, m.start()-200)
        end=min(len(t), m.end()+500)
        snippet=t[start:end]
        print("--- at", m.start())
        print(snippet[:700])
        print("---")
# show structure around first package entry
idxs=[m.start() for m in re.finditer(r"package=|pkg=|<package|<item|<app", t)]
print("\nstructure hits sample", idxs[:15])
print("root tags", re.findall(r"</?\w+[^>]*>", t[:800])[:30])
