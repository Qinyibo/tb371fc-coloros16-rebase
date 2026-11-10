import sqlite3, shutil, os
p = r"E:\youxikaifa\work\fantasywindow.db"
bak = p + ".bak"
if not os.path.exists(bak):
    shutil.copy2(p, bak)
con = sqlite3.connect(p)
cur = con.cursor()
cur.execute("delete from t_config where package_name='tv.danmaku.bili' and use_function='magicwindow'")
con.commit()
print("deleted rows:", cur.rowcount)
for row in cur.execute("select package_name, use_function, status, custom_mode from t_config where package_name='tv.danmaku.bili'"):
    print("remaining:", row)
con.close()
