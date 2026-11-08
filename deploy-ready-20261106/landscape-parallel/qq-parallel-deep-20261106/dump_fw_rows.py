import sqlite3, json
db=r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\qq-parallel-deep-20261106\fantasywindow.live.db"
con=sqlite3.connect(db)
cur=con.cursor()
print("TABLES:", [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")])
for t in ['t_config','t_server','t_sign']:
    cols=[d[1] for d in cur.execute(f"PRAGMA table_info({t})").fetchall()]
    print(f"\n## {t} cols={cols}")
    pkgcol=None
    for c in cols:
        cl=c.lower()
        if 'package' in cl or cl in ('pkg','name','pkg_name','package_name'):
            pkgcol=c; break
    if not pkgcol:
        rows=cur.execute(f"SELECT * FROM {t} LIMIT 3").fetchall()
        print("sample", rows)
        continue
    for pkg in ('com.tencent.mobileqq','com.tencent.mm','com.tencent.tim'):
        rows=cur.execute(f"SELECT * FROM {t} WHERE {pkgcol}=?", (pkg,)).fetchall()
        if not rows: continue
        print(f"--- {pkg} rows={len(rows)}")
        for row in rows:
            d=dict(zip(cols,row))
            for k,v in list(d.items()):
                if isinstance(v,str) and len(v)>800:
                    d[k]=v[:800]+f"...<{len(v)}>"
            print(json.dumps(d, ensure_ascii=False, indent=2))
