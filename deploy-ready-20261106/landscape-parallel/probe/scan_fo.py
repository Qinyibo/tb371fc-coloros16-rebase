import zipfile, re, collections
from pathlib import Path
jar = Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\oplus-services.jar")
out = Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\fo-strings.txt")
keys = [b"FullOrientation", b"fullorientation", b"alwaysFullOrient", b"mIsFullOrientation", b"rao", b"AppLandscape", b"ignoreOrientation"]
hits=[]
with zipfile.ZipFile(jar) as z:
    names=z.namelist()
    out.write_text("entries "+str(len(names))+"\n", encoding="utf-8")
    for n in names:
        if not (n.endswith(".dex") or "FullOrient" in n or "Fantasy" in n or "Flexible" in n):
            # still scan all dex
            if not n.endswith(".dex"):
                continue
        data=z.read(n)
        for k in keys:
            for m in re.finditer(re.escape(k)+b".{0,80}", data):
                try:
                    s=m.group().decode("utf-8","replace")
                except: s=repr(m.group())
                hits.append(n+": "+s)
        # also class names
        for m in re.finditer(rb"Lcom/android/server/wm/[A-Za-z0-9_]*FullOrient[A-Za-z0-9_]*;|Lcom/android/server/wm/[A-Za-z0-9_]*Fantasy[A-Za-z0-9_]*;|Lcom/oplus/[A-Za-z0-9_/]*FullOrient[A-Za-z0-9_]*;", data):
            hits.append(n+": CLASS "+m.group().decode("utf-8","replace"))
# unique preserve order
seen=set(); uniq=[]
for h in hits:
    if h not in seen:
        seen.add(h); uniq.append(h)
out.write_text("\n".join(uniq[:400]), encoding="utf-8")
print("hits", len(uniq))
print("\n".join(uniq[:80]))
