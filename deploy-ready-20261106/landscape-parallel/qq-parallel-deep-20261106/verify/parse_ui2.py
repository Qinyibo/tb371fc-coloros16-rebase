import re, pathlib
t=pathlib.Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\qq-parallel-deep-20261106\verify\qq-ui2.xml").read_text(encoding="utf-8",errors="ignore")
print("len",len(t))
# all nodes with text or content-desc and bounds
pat=re.compile(r'node [^>]*?(?:text="([^"]*)")?[^>]*?(?:content-desc="([^"]*)")?[^>]*?clickable="true"[^>]*?bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"')
# looser: any bounds
nodes=re.findall(r'<(?:node)([^>]*)>', t)
cands=[]
for attrs in nodes:
    def g(k):
        m=re.search(k+r'="([^"]*)"', attrs)
        return m.group(1) if m else ''
    text=g('text'); cd=g('content-desc'); clk=g('clickable'); b=g('bounds')
    m=re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', b)
    if not m: continue
    x1,y1,x2,y2=map(int,m.groups())
    label=(text or cd).strip()
    if clk=='true' and label and x2<=1100 and y1>80:
        cands.append((label,x1,y1,x2,y2,(x1+x2)//2,(y1+y2)//2))
print('left-pane clickables', len(cands))
for c in cands[:30]:
    print(c)
