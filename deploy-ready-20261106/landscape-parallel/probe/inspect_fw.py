import sqlite3, json, os
p = r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\fw-live.db"
c = sqlite3.connect(p)
print("tables:")
for r in c.execute("select name from sqlite_master where type='table'"):
    print(" ", r[0])
    cols = c.execute(f"pragma table_info({r[0]})").fetchall()
    print("  cols:", cols)
print("--- aweme rows ---")
for r in c.execute("select name from sqlite_master where type='table'"):
    t=r[0]
    cols=[x[1] for x in c.execute(f"pragma table_info({t})").fetchall()]
    if not cols: continue
    # try find package-like columns
    qcols=",".join(cols)
    try:
        rows=c.execute(f"select * from {t}").fetchall()
    except Exception as e:
        print(t, e); continue
    for row in rows:
        s=str(row)
        if "aweme" in s or "fullorient" in s.lower() or "full_orient" in s.lower():
            print(t, dict(zip(cols,row)) if len(cols)==len(row) else row)
print("--- function counts ---")
# heuristic: print distinct use_function if present
for t in [x[0] for x in c.execute("select name from sqlite_master where type='table'")]:
    cols=[x[1] for x in c.execute(f"pragma table_info({t})").fetchall()]
    if "use_function" in cols and "package_name" in cols:
        print(t, "use_function values:", c.execute(f"select use_function, count(*), sum(case when status=1 then 1 else 0 end) as on_cnt from {t} group by use_function").fetchall())
        print("aweme:", c.execute(f"select package_name, use_function, status, config, func_version from {t} where package_name like '%aweme%'").fetchall())
        print("sample status meanings for mm:", c.execute(f"select package_name, use_function, status, substr(config,1,120) from {t} where package_name='com.tencent.mm'").fetchall())
