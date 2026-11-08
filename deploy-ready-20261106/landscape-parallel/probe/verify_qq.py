import sqlite3
db=r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\fw-after-qq.db"
c=sqlite3.connect(db)
print("QQ:")
for r in c.execute("SELECT use_function,status,config,substr(coalesce(custom_config_body,''),1,100) FROM t_config WHERE package_name='com.tencent.mobileqq'"):
    print(r)
print("aweme:")
for r in c.execute("SELECT use_function,status,config FROM t_config WHERE package_name='com.ss.android.ugc.aweme'"):
    print(r)
