import sqlite3
c=sqlite3.connect(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\fw-live.db")
print("installed magic any status:", c.execute("select status,count(*) from t_config where use_function='magicwindow' and installed=1 group by status").fetchall())
print("installed fullorient any:", c.execute("select status,count(*) from t_config where use_function='fullorientation' and installed=1 group by status").fetchall())
print("installed compact any:", c.execute("select status,count(*) from t_config where use_function='compactwindow' and installed=1 group by status").fetchall())
print("ALL installed magic rows:")
for r in c.execute("select package_name,status,substr(config,1,100) from t_config where use_function='magicwindow' and installed=1 order by status, package_name"):
    print(r)
print("ALL installed fullorient:")
for r in c.execute("select package_name,status,substr(custom_config_body,1,100) from t_config where use_function='fullorientation' and installed=1 order by status, package_name"):
    print(r)
