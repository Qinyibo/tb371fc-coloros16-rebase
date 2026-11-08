import json, re, pathlib, shutil, sqlite3, hashlib
root=pathlib.Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\qq-parallel-deep-20261106")
payload=root/"payload"
# v3: WeChat UX ratios + real chat pairs, NO relatedPage/GuildBlank, NO supportAppTaskSplitScreen, NO changeToFullscreen
cfg={
  "mode":"1",
  "defSwitch":"magic",
  "ignoreCameraRotation":"true",
  "isRelaunchwhenResize":"false",
  "scaleWindow":"-1",
  "noRelaunchOnResize":"true",
  "activityPairs":[
    {"from":"com.tencent.mobileqq.activity.SplashActivity","to":"*"},
    {"from":"com.tencent.mobileqq.activity.SplashActivity","to":"com.tencent.mobileqq.activity.ChatActivity"},
    {"from":"com.tencent.mobileqq.activity.SplashActivity","to":"com.tencent.aio.main.activity.ChatActivity"},
    {"from":"com.tencent.mobileqq.activity.SplashActivity","to":"com.tencent.qqnt.aio.localactivity.AIOLocalActivity"},
    {"from":"com.tencent.mobileqq.activity.SplashActivity","to":"com.tencent.mobileqq.activity.miniaio.MiniChatActivity"},
    {"from":"com.tencent.mobileqq.activity.SplashActivity","to":"com.tencent.mobileqq.activity.PublicFragmentActivity"},
    {"from":"com.tencent.mobileqq.activity.SplashActivity","to":"com.tencent.mobileqq.activity.QPublicFragmentActivity"}
  ],
  "transActivities":["com.tencent.mobileqq.activity.LoginActivity"],
  "Activities":[
    {"name":"com.tencent.mobileqq.activity.ChatActivity","forceRelaunch":"true"},
    {"name":"com.tencent.aio.main.activity.ChatActivity","forceRelaunch":"true"},
    {"name":"com.tencent.qqnt.aio.localactivity.AIOLocalActivity","forceRelaunch":"true"},
    {"name":"com.tencent.mobileqq.activity.miniaio.MiniChatActivity","forceRelaunch":"true"},
    {"name":"*","reverseCameraRotation":"10","reverseCameraRotationFront":"9"}
  ],
  "UX":{
    "isDraggable":"true",
    "showStatusBar":"true",
    "keepPrimaryTopAlwaysResume":"true",
    "useSystemActivityAnimation":"false",
    "windowsRatio":[
      {"device":"PAD","ratio":"900|1654"},
      {"device":"FOLD","ratio":"1056|1138"}
    ],
    "splitLineBgColor":"0xff191919",
    "splitBarBgColor":"0xffe5e5e5"
  }
}
js=json.dumps(cfg,ensure_ascii=False,separators=(',',':'))
(payload/"qq-magic-v3.json").write_text(js,encoding='utf-8')
caret=js.replace('"','^')
(payload/"qq-magic-v3.caret.txt").write_text(caret,encoding='utf-8')
# patch from current live-pulled base (v2 currently on device) using host copy of live before v2? Use v2 xml as base replace mobileqq line
src=payload/"sys_fantasy_window_managed.qq-v2.xml"
text=src.read_text(encoding='utf-8')
pat=re.compile(r'<a package_name="com\.tencent\.mobileqq" status="[^"]*" func_version="[^"]*" use_function="magicwindow" custom_config_body="[^"]*"\s*/>')
repl=f'<a package_name="com.tencent.mobileqq" status="1" func_version="1.5" use_function="magicwindow" custom_config_body="{caret}" />'
new,n=pat.subn(repl,text,count=1)
assert n==1, n
dst=payload/"sys_fantasy_window_managed.qq-v3.xml"
dst.write_text(new,encoding='utf-8')
print('xml md5', hashlib.md5(dst.read_bytes()).hexdigest(), 'json_len', len(js))
# DB from fantasywindow.live.db original pull
db_src=root/"fantasywindow.live.db"
db_dst=payload/"fantasywindow.qq-v3.db"
shutil.copy2(db_src, db_dst)
con=sqlite3.connect(db_dst)
cur=con.cursor()
cur.execute("UPDATE t_config SET config=?, custom_config_body=?, status=1, custom_mode=-1, data_sources=2, func_version='1.5' WHERE package_name='com.tencent.mobileqq' AND use_function='magicwindow'", (js,js))
print('db rows', cur.rowcount, 'cfg_len', len(js))
con.commit(); con.close()
