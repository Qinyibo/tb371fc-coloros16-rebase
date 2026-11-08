import sqlite3
c=sqlite3.connect(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\fantasywindow.after.db")
print(c.execute("SELECT status,config FROM t_config WHERE package_name='com.ss.android.ugc.aweme' AND use_function='magicwindow'").fetchone())
