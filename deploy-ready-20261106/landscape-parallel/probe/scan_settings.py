import pathlib,re
base=pathlib.Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe")
pat=re.compile(r'tablet|phone|density|ratio|compact|pad|landscape|display_size|app_ratio|force|swdp|xlarge|characteristics|device_type', re.I)
for name in ['settings-system.txt','settings-global.txt','settings-secure.txt']:
    print('====', name)
    t=(base/name).read_text(encoding='utf-8-sig', errors='replace')
    for line in t.splitlines():
        if pat.search(line):
            print(line)
