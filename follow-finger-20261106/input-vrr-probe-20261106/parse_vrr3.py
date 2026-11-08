import json,pprint
p=r'D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\input-vrr-probe-20261106\oplus_vrr_config.live.json'
j=json.load(open(p,encoding='utf-8-sig'))
# dump items 3,5,6,7,9 fully
for i in [3,5,6,7,9]:
    print('='*20,'ITEM',i,'='*20)
    pprint.pp(j[i], width=140, compact=False)
