import sqlite3, json
db=r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\qq-parallel-deep-20261106\fantasywindow.live.db"
con=sqlite3.connect(db)
cur=con.cursor()
for pkg,fn in [('com.tencent.mm','magicwindow'),('com.tencent.mobileqq','magicwindow')]:
    row=cur.execute("SELECT config, custom_config_body, status, custom_mode, data_sources FROM t_config WHERE package_name=? AND use_function=?", (pkg,fn)).fetchone()
    cfg, body, st, cm, ds = row
    open(rf"{r'D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\qq-parallel-deep-20261106\verify'}\{pkg}.{fn}.config.json",'w',encoding='utf-8').write(cfg or '')
    open(rf"{r'D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\qq-parallel-deep-20261106\verify'}\{pkg}.{fn}.custom_body.json",'w',encoding='utf-8').write(body or '')
    print(pkg, 'status',st,'custom_mode',cm,'ds',ds,'config_len',len(cfg or ''),'body_len',len(body or ''))
    if cfg:
        try:
            j=json.loads(cfg)
            print(' keys', sorted(j.keys()))
            if 'activityPairs' in j: print(' activityPairs', json.dumps(j['activityPairs'], ensure_ascii=False)[:1000])
            if 'UX' in j: print(' UX', json.dumps(j['UX'], ensure_ascii=False)[:800])
            for k in ['supportAppTaskSplitScreen','scaleWindow','defSwitch','mode','force_custom_pw_mode','changeToFullscreen','mainPage','relatedPage']:
                if k in j: print(' ',k,'=',j[k])
        except Exception as e:
            print('parse err',e)
