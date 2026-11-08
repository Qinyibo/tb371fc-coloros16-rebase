import sqlite3
c=sqlite3.connect(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\fw-live.db")
print("magic on installed:", c.execute("select count(*) from t_config where use_function='magicwindow' and status=1 and installed=1").fetchone()[0])
print("magic on total:", c.execute("select count(*) from t_config where use_function='magicwindow' and status=1").fetchone()[0])
print("fullorient on installed:", c.execute("select count(*) from t_config where use_function='fullorientation' and status=1 and installed=1").fetchone()[0])
print("fullorient status2 installed:", c.execute("select count(*) from t_config where use_function='fullorientation' and status=2 and installed=1").fetchone()[0])
print("sample fullorient status1 installed:")
for r in c.execute("select package_name,status,substr(custom_config_body,1,80) from t_config where use_function='fullorientation' and status=1 and installed=1 limit 15"):
    print(r)
