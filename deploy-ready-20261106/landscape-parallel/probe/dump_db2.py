import sqlite3, shutil, os
base = r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe"
# assemble proper sqlite files
shutil.copy(os.path.join(base,"canvas_db.bin"), os.path.join(base,"canvas.db"))
shutil.copy(os.path.join(base,"canvas_db.wal"), os.path.join(base,"canvas.db-wal"))
shutil.copy(os.path.join(base,"canvas_db.shm"), os.path.join(base,"canvas.db-shm"))
c = sqlite3.connect(os.path.join(base,"canvas.db"))
print("master:", c.execute("SELECT name,sql FROM sqlite_master").fetchall())
for (t,) in c.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    cols = c.execute(f"PRAGMA table_info([{t}])").fetchall()
    print("TABLE", t, "cols", cols)
    rows = c.execute(f"SELECT * FROM [{t}]").fetchall()
    print(" rows", len(rows))
    for r in rows[:50]:
        print(" ", r)
    # search aweme
    for col in cols:
        try:
            hits = c.execute(f"SELECT * FROM [{t}] WHERE CAST([{col[1]}] AS TEXT) LIKE '%aweme%' OR CAST([{col[1]}] AS TEXT) LIKE '%抖音%'").fetchall()
            if hits:
                print(" AWEME HITS in", col[1], hits)
        except Exception as e:
            pass
