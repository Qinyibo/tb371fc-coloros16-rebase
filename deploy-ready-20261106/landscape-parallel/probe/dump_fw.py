import sqlite3, os
p = r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\fantasywindow.db"
c = sqlite3.connect(p)
print("master:")
for row in c.execute("SELECT name,sql FROM sqlite_master"):
    print(row[0], "=>", row[1][:200] if row[1] else None)
for (t,) in c.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    cols = [x[1] for x in c.execute(f"PRAGMA table_info([{t}])")]
    n = c.execute(f"SELECT COUNT(*) FROM [{t}]").fetchone()[0]
    print(f"\nTABLE {t} ({n} rows) cols={cols}")
    # aweme hits
    for col in cols:
        try:
            hits = c.execute(f"SELECT * FROM [{t}] WHERE CAST([{col}] AS TEXT) LIKE '%aweme%'").fetchall()
            if hits:
                print(f"  AWEME via {col}:")
                for h in hits[:20]:
                    print("   ", h)
        except Exception as e:
            print("  err", col, e)
    if n <= 30 and n > 0 and t not in ('android_metadata','room_master_table'):
        print("  ALL:")
        for r in c.execute(f"SELECT * FROM [{t}]").fetchall()[:30]:
            print("   ", r)
