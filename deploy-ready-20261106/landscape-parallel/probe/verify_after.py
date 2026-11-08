import sqlite3
c=sqlite3.connect(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\fw-after-native.db")
print(c.execute("select use_function,status,config from t_config where package_name='com.ss.android.ugc.aweme'").fetchall())
