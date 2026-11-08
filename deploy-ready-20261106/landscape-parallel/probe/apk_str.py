import zipfile, re
from pathlib import Path
apk=Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\OplusFlexibleWindowUI.apk")
out=Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\pscanvas-strings.txt")
words=set()
with zipfile.ZipFile(apk) as z:
    # resources arsc / xml and dex
    for n in z.namelist():
        data=z.read(n)
        # chinese + english keywords
        for m in re.finditer(r'[\u4e00-\u9fff]{2,20}'.encode('utf-8'), data):
            try: words.add(m.group().decode('utf-8'))
            except: pass
        for m in re.finditer(rb'(Parallel|Flexible|Magic|Zoom|Canvas|Layout|Ratio|AutoLayout|FullOrient|GameList|Operation|Setting)[A-Za-z0-9_]{0,30}', data):
            words.add(m.group().decode('utf-8','replace'))
# filter interesting
keys=['平行','视界','横屏','布局','分屏','比例','自适应','应用','游戏','画布','窗口','悬浮','全屏','魔法']
cjk=[w for w in words if any(k in w for k in keys)]
eng=[w for w in words if re.match(r'^(Parallel|Flexible|Magic|Zoom|Canvas|Layout|Ratio|AutoLayout|FullOrient|GameList|Operation)', w)]
lines=sorted(cjk)+['---']+sorted(eng)[:80]
out.write_text('\n'.join(lines), encoding='utf-8')
print('cjk', len(cjk))
print('\n'.join(sorted(cjk)[:60]))
print('--- eng ---')
print('\n'.join(sorted(eng)[:40]))
