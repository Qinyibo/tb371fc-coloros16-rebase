import json,re
p=r'D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\input-vrr-probe-20261106\oplus_vrr_config.live.json'
raw=open(p,'r',encoding='utf-8').read()
try:
    j=json.loads(raw)
    print('JSON_OK type',type(j).__name__)
    if isinstance(j,dict):
        print('TOP_KEYS',list(j.keys())[:50])
except Exception as e:
    print('JSON_FAIL',e); j=None

for pkg in ['com.tencent.mm','com.ss.android.ugc.aweme','com.luna.music','adfr_enable','sw_whitelist','hw_whitelist','game_whitelist']:
    idx=0; n=0
    while n<10:
        i=raw.find(pkg, idx)
        if i<0: break
        print('---',pkg,'@',i,'---')
        print(raw[max(0,i-160):i+280].replace('\n',' '))
        idx=i+len(pkg); n+=1
