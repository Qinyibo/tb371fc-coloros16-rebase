import sqlite3
p = r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\canvas_task_database"
c = sqlite3.connect(p)
print("master:", c.execute("SELECT name,sql FROM sqlite_master").fetchall())
for (t,) in c.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    print("TABLE", t)
    print(c.execute(f"SELECT * FROM [{t}]").fetchall())
