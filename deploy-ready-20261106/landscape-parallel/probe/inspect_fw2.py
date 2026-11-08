import sqlite3, pprint
p = r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\fw-live.db"
c = sqlite3.connect(p)
for t in [x[0] for x in c.execute("select name from sqlite_master where type='table'")]:
    cols=[x[1] for x in c.execute("pragma table_info(%s)"%t).fetchall()]
    if "package_name" not in cols:
        continue
    rows=c.execute("select * from %s where package_name like '%%aweme%%'"%t).fetchall()
    if not rows:
        continue
    print("TABLE", t)
    print("COLS", cols)
    for r in rows:
        pprint.pp(dict(zip(cols,r)))
for t in [x[0] for x in c.execute("select name from sqlite_master where type='table'")]:
    cols=[x[1] for x in c.execute("pragma table_info(%s)"%t).fetchall()]
    if "use_function" in cols and "status" in cols:
        print("COUNTS", t)
        pprint.pp(c.execute("select use_function, status, count(*) from %s group by use_function, status order by 1,2"%t).fetchall())
        print("WeChat:")
        pprint.pp(c.execute("select package_name, use_function, status, config from %s where package_name='com.tencent.mm'"%t).fetchall())
