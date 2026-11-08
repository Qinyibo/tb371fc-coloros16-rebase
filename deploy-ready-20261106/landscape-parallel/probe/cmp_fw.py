import sqlite3
p = r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\fantasywindow.db"
c = sqlite3.connect(p)
pkgs = ['com.tencent.mm','tv.danmaku.bili','com.ss.android.ugc.aweme','cn.wps.moffice_eng','com.smile.gifmaker']
for pkg in pkgs:
    print('====', pkg)
    for r in c.execute("SELECT package_name,use_function,status,custom_mode,config,substr(custom_config_body,1,180),func_version,installed FROM t_config WHERE package_name=?", (pkg,)):
        print(r)
# status distribution for magicwindow installed
print('\nstatus counts magicwindow installed:')
for r in c.execute("SELECT status, COUNT(*) FROM t_config WHERE use_function='magicwindow' AND installed=1 GROUP BY status"):
    print(r)
print('\nsample status=1 magicwindow:')
for r in c.execute("SELECT package_name,status,config FROM t_config WHERE use_function='magicwindow' AND installed=1 AND status=1 LIMIT 10"):
    print(r)
print('\nsample status=2 magicwindow:')
for r in c.execute("SELECT package_name,status,config FROM t_config WHERE use_function='magicwindow' AND installed=1 AND status=2 LIMIT 10"):
    print(r)
