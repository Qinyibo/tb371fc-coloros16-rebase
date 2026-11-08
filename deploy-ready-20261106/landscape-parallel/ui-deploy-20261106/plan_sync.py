import sqlite3,re,os
out=r'D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\ui-deploy-20261106'
pkgs=set()
for line in open(out+r'\installed-all.txt',encoding='ascii',errors='ignore'):
    m=re.match(r'package:(.+)', line.strip())
    if m: pkgs.add(m.group(1).strip())
print('pkgs',len(pkgs))
dbpath=out+r'\fantasywindow.pre-sync.db'
print('db',os.path.getsize(dbpath))
db=sqlite3.connect(dbpath)
c=db.cursor()
rows=list(c.execute("SELECT package_name,status,installed,length(coalesce(config,'')) FROM t_config WHERE use_function='magicwindow'"))
need=[]; already=[]
for pkg,st,inst,cfglen in rows:
    if pkg in pkgs:
        (already if inst==1 else need).append((pkg,st,cfglen))
print('magic_total',len(rows))
print('on_device_magic',len(need)+len(already))
print('already_installed1',len(already))
for x in already: print('OK',x)
print('need_mark',len(need))
for x in need: print('MARK',x)
# FO pairing
print('FO pairing for on-device magic:')
for pkg,st,cfglen in already+need:
    fo=c.execute("SELECT status FROM t_config WHERE package_name=? AND use_function='fullorientation'",(pkg,)).fetchone()
    print(pkg,'MW',st,'cfg',cfglen,'FO', fo[0] if fo else None)
