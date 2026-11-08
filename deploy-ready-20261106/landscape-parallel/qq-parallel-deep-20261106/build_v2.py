import json, re, pathlib, sqlite3, hashlib
root=pathlib.Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\qq-parallel-deep-20261106")
payload=root/"payload"
cfg={
  "mode":"1",
  "defSwitch":"magic",
  "ignoreCameraRotation":"true",
  "isRelaunchwhenResize":"false",
  "supportAppTaskSplitScreen":"true",
  "scaleWindow":"-1",
  "noRelaunchOnResize":"true",
  "activityPairs":[
    {"from":"com.tencent.mobileqq.activity.SplashActivity","to":"*"},
    {"mainPage":"com.tencent.mobileqq.activity.SplashActivity","relatedPage":"com.tencent.mobileqq.guild.base.GuildBlankActivity"},
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
(payload/"qq-magic-v2.json").write_text(js,encoding='utf-8')
caret=js.replace('"','^')
(payload/"qq-magic-v2.caret.txt").write_text(caret,encoding='utf-8')
src=root/"sys_fantasy_window_managed.live.xml"
dst=payload/"sys_fantasy_window_managed.qq-v2.xml"
text=src.read_text(encoding='utf-8')
pat=re.compile(r'<a package_name="com\.tencent\.mobileqq" status="[^"]*" func_version="[^"]*" use_function="magicwindow" custom_config_body="[^"]*"\s*/>')
repl=f'<a package_name="com.tencent.mobileqq" status="1" func_version="1.5" use_function="magicwindow" custom_config_body="{caret}" />'
new,n=pat.subn(repl,text,count=1)
if n!=1:
    raise SystemExit(f'replace count={n}')
dst.write_text(new,encoding='utf-8')
print('xml_size', dst.stat().st_size, 'json_len', len(js), 'md5', hashlib.md5(dst.read_bytes()).hexdigest())
# also prepare DB update SQL values
print('JSON=', js[:200])
