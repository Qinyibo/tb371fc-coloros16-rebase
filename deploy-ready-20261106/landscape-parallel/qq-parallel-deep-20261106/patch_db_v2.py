import sqlite3, json, pathlib, shutil
root=pathlib.Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\qq-parallel-deep-20261106")
src=root/"fantasywindow.live.db"
dst=root/"payload"/"fantasywindow.qq-v2.db"
shutil.copy2(src,dst)
cfg=(root/"payload"/"qq-magic-v2.json").read_text(encoding='utf-8').strip()
con=sqlite3.connect(dst)
cur=con.cursor()
cur.execute("UPDATE t_config SET config=?, custom_config_body=?, status=1, custom_mode=-1, data_sources=2, func_version='1.5' WHERE package_name='com.tencent.mobileqq' AND use_function='magicwindow'", (cfg,cfg))
print('rows', cur.rowcount)
row=cur.execute("SELECT length(config), status, custom_mode, substr(config,1,120) FROM t_config WHERE package_name='com.tencent.mobileqq' AND use_function='magicwindow'").fetchone()
print(row)
con.commit(); con.close()
