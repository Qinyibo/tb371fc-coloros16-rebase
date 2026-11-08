from pathlib import Path
import re
t=Path(r"D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\fluency-headroom-20261106-2038\refresh_rate_config.xml").read_text(encoding="utf-8",errors="replace")
for pat in ["Version","defaultRateId","maxRefreshRateId","maxrefreshsettings","defaultMaxRate","AppSwitchBoost","mAppSwitch"]:
    for m in re.finditer(pat+r'[^<\n]{0,80}', t):
        print(m.group()[:120])
# count rate entries
print("len", len(t))
print("count 144", t.count("144"))
print("count rateId=\"4\"", t.count('rateId="4"'))
