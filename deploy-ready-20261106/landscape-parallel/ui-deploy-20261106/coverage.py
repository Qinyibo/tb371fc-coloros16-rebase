import os,re,sqlite3
out=r'D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\ui-deploy-20261106'
third=set()
for line in open(out+r'\installed-3rd.txt',encoding='ascii',errors='ignore'):
    m=re.match(r'package:(.+)', line.strip())
    if m: third.add(m.group(1).strip())
db=sqlite3.connect(out+r'\fantasywindow.pre-sync.db')
c=db.cursor()
print('=== 3rd party magic/FO coverage ===')
missing_mw=[]
for pkg in sorted(third):
    mw=c.execute("SELECT status,installed,length(coalesce(config,'')) FROM t_config WHERE package_name=? AND use_function='magicwindow'",(pkg,)).fetchone()
    fo=c.execute("SELECT status,installed FROM t_config WHERE package_name=? AND use_function='fullorientation'",(pkg,)).fetchone()
    print(pkg,'MW',mw,'FO',fo)
    if not mw: missing_mw.append(pkg)
print('missing_mw',len(missing_mw),missing_mw)

# Check product XML for those missing
fantasy_dir=os.path.join(out,'product-fantasy-live')
xmls=[]
for root,dirs,files in os.walk(fantasy_dir):
  for f in files:
    if f.endswith('.xml'): xmls.append(os.path.join(root,f))
print('xmls',xmls)
text=''
for p in xmls:
  try: text+=open(p,encoding='utf-8',errors='ignore').read()
  except: pass
for pkg in missing_mw:
    hit=pkg in text
    print('xml_has',pkg,hit)
