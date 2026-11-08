import sqlite3, shutil, os
base = r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe"
src = os.path.join(base, "fantasywindow.db")
dst = os.path.join(base, "fantasywindow.patched.db")
shutil.copy2(src, dst)
c = sqlite3.connect(dst)
cur = c.cursor()
row = cur.execute("SELECT status,config,custom_config_body FROM t_config WHERE package_name=? AND use_function=?",
                  ("com.ss.android.ugc.aweme","magicwindow")).fetchone()
print("BEFORE magicwindow:", row[0], row[1])
# Enable magicwindow on PAD: status=1, drop excludeDevice
cur.execute("UPDATE t_config SET status=1, config=? WHERE package_name=? AND use_function=?",
            ('{"mode":"1"}', "com.ss.android.ugc.aweme", "magicwindow"))
# Also set fullorientation to not force SplashActivity portrait-only if possible —
# leave fullorientation for now; magicwindow is the parallel path.
row2 = cur.execute("SELECT status,config FROM t_config WHERE package_name=? AND use_function=?",
                   ("com.ss.android.ugc.aweme","magicwindow")).fetchone()
print("AFTER magicwindow:", row2)
c.commit()
c.close()
print("patched ->", dst)
