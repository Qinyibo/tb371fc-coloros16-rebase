import zipfile, re
from pathlib import Path
jar = Path(r"D:\TB371FC-release\clean-rebase-20261104\donor-tree\system\system\framework\oplus-services.jar")
out = Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\fo-strings.txt")
hits=[]
with zipfile.ZipFile(jar) as z:
    for n in z.namelist():
        if not n.endswith('.dex'): continue
        data=z.read(n)
        for pat in [rb'FullOrientation[A-Za-z0-9_]{0,40}', rb'alwaysFullOrient[A-Za-z0-9_]{0,40}', rb'isFullOrientation[A-Za-z0-9_]{0,60}', rb'fullorientation', rb'AppLandscape[A-Za-z0-9_]{0,40}', rb'shouldOverrideOrientation[A-Za-z0-9_]{0,40}', rb'forceFullOrientation[A-Za-z0-9_]{0,40}', rb'mStatus\s*==\s*1', rb'STATUS_ENABLE', rb'getFullOrientation']:
            for m in re.finditer(pat, data):
                s=m.group().decode('utf-8','replace')
                # context
                start=max(0,m.start()-40); end=min(len(data), m.end()+60)
                ctx=data[start:end]
                ctx=''.join(chr(b) if 32<=b<127 else '.' for b in ctx)
                hits.append(f"{n}: {s} | {ctx}")
seen=set(); uniq=[]
for h in hits:
    if h not in seen:
        seen.add(h); uniq.append(h)
out.write_text('\n'.join(uniq[:500]), encoding='utf-8')
print('hits', len(uniq))
for h in uniq[:100]:
    print(h[:220])
