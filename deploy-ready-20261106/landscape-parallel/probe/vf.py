import sqlite3
c=sqlite3.connect(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\fw-final.db")
print("FINAL", c.execute("select use_function,status,config,custom_config_body from t_config where package_name='com.ss.android.ugc.aweme' and use_function in ('magicwindow','fullorientation')").fetchall())
