import sqlite3, pprint, json
p = r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\fw-live.db"
out = r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\fw-summary.txt"
c = sqlite3.connect(p)
lines=[]
for t in [x[0] for x in c.execute("select name from sqlite_master where type='table'")]:
    cols=[x[1] for x in c.execute("pragma table_info(%s)"%t).fetchall()]
    lines.append("TABLE %s COLS %s"%(t,cols))
    if "package_name" in cols:
        rows=c.execute("select * from %s where package_name like '%%aweme%%'"%t).fetchall()
        for r in rows:
            d=dict(zip(cols,r))
            # truncate long config
            if "config" in d and d["config"] and len(str(d["config"]))>200:
                d["config"]=str(d["config"])[:200]+"..."
            if "custom_config_body" in d and d["custom_config_body"] and len(str(d["custom_config_body"]))>200:
                d["custom_config_body"]=str(d["custom_config_body"])[:200]+"..."
            lines.append("AWEME "+json.dumps(d, ensure_ascii=False))
    if "use_function" in cols and "status" in cols:
        lines.append("COUNTS "+str(c.execute("select use_function, status, count(*) from %s group by use_function, status order by 1,2"%t).fetchall()))
        mm=c.execute("select package_name, use_function, status, substr(coalesce(config,''),1,160) from %s where package_name='com.tencent.mm'"%t).fetchall()
        lines.append("WECHAT "+str(mm))
        bili=c.execute("select package_name, use_function, status, substr(coalesce(config,''),1,160) from %s where package_name='tv.danmaku.bili'"%t).fetchall()
        lines.append("BILI "+str(bili))
open(out,"w",encoding="utf-8").write("\n".join(lines))
print("wrote", out, "lines", len(lines))
