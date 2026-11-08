import sqlite3
c=sqlite3.connect(r"D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\fluency-headroom-20261106-2038\fw-check.db")
print(c.execute("select use_function,status,config from t_config where package_name='com.ss.android.ugc.aweme' and use_function in ('magicwindow','fullorientation')").fetchall())
