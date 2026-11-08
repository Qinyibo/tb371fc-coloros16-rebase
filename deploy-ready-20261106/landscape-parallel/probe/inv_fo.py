from pathlib import Path
import re, json
base = Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe")
fo = (base/"sys_full_orientation_managed.live.xml").read_text(encoding="utf-8", errors="replace")
# entries: <o package_name="..." status="N" ... custom_config_body="..." />
pat = re.compile(r'<o\s+package_name="([^"]+)"\s+status="(\d)"\s+use_function="([^"]*)"\s+custom_config_body="([^"]*)"\s*/?>')
rows = pat.findall(fo)
print("FO entries", len(rows))
from collections import Counter
print("status counts", Counter(s for _,s,_,_ in rows))
# installed -3
pkgs3 = [ln.split(":",1)[1].strip() for ln in (base/"pkgs-user3.txt").read_text(encoding="utf-8",errors="replace").splitlines() if ln.startswith("package:")]
print("user3", len(pkgs3))
# also pull all packages that look third-party / popular
# show FO status for each installed -3
print("\n=== installed -3 FO status ===")
fo_map = {p:(s,fn,body) for p,s,fn,body in rows}
for p in pkgs3:
    if p in fo_map:
        s,fn,body = fo_map[p]
        print(f"{p}\tstatus={s}\tbody={body[:120]}")
    else:
        print(f"{p}\tNOT_IN_FO_XML")

# special apps of interest even if system
interest = ["com.tencent.mm","com.tencent.mobileqq","com.ss.android.ugc.aweme","com.luna.music",
"com.android.browser","com.heytap.browser","com.oplus.browser","com.android.chrome",
"com.baidu.BaiduMap","com.autonavi.minimap","com.tencent.map",
"com.youku.phone","com.qiyi.video","tv.danmaku.bili","com.ss.android.article.news",
"com.ss.android.ugc.aweme.lite","com.smile.gifmaker","com.kuaishou.nebula",
"com.netease.cloudmusic","com.tencent.qqmusic","com.xingin.desktop",
"cn.wps.moffice_eng","com.oplus.wpslauncher","com.heytap.yoli","com.heytap.music",
"com.coloros.gallery3d","com.oneplus.gallery","com.oplus.gallery",
"com.ss.android.ugc.live","com.ss.android.article.video"]
print("\n=== interest FO ===")
for p in interest:
    if p in fo_map:
        s,fn,body = fo_map[p]
        print(f"{p}\tstatus={s}\tbody={body[:160]}")
    else:
        print(f"{p}\tNOT_IN_FO_XML")

# rao true ones
rao_true = [p for p,s,fn,b in rows if "rao^:^true" in b or 'rao":"true' in b.replace("^",'"')]
print("\nrao=true count", len(rao_true))
print("rao=true samples", rao_true[:20])
status0 = [p for p,s,_,_ in rows if s=="0"]
status2 = [p for p,s,_,_ in rows if s=="2"]
print("status0", len(status0), "status2", len(status2))
print("status0 sample", status0[:30])
print("status2 sample", status2[:30])
