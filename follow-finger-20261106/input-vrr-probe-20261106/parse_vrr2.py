import json,pprint
p=r'D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\input-vrr-probe-20261106\oplus_vrr_config.live.json'
j=json.load(open(p,encoding='utf-8-sig'))
print('type',type(j))
if isinstance(j,list):
    for i,item in enumerate(j):
        print('ITEM',i,'keys',list(item.keys()) if isinstance(item,dict) else type(item))
        if isinstance(item,dict):
            for k in ['adfr_enable','sw_enable','hw_enable','touch_idle','hw_lowest_rate','timeout','sw_whitelist_3rd','sw_whitelist','hw_whitelist','blacklist','version','sub_version']:
                if k in item: print(' ',k,':',item[k] if k!='blacklist' else str(item[k])[:200])
elif isinstance(j,dict):
    print(list(j.keys())[:40])
    pprint.pp(j, depth=3, width=120)
