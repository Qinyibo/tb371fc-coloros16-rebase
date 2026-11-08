import re, sqlite3, shutil, hashlib, json, os
base = r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\qq-oldrestore-20261106\payload"
src_xml = os.path.join(base, "sys_fantasy_window_managed.pre.xml")
dst_xml = os.path.join(base, "sys_fantasy_window_managed.oldrestore.xml")
src_db = os.path.join(base, "fantasywindow.pre.db")
dst_db = os.path.join(base, "fantasywindow.oldrestore.db")
fo_src = os.path.join(base, "sys_full_orientation_managed.live.xml")
fo_dst = os.path.join(base, "sys_full_orientation_managed.oldrestore.xml")

# Exact old product body (caret form) from R94 secondary / old DB forceBlock
OLD_BODY_CARET = (
    "{^Activities^:[{^name^:^*^,^reverseCameraRotation^:^10^,^reverseCameraRotationFront^:^9^}],"
    "^noRelaunchOnResize^:^true^,^adjustDisplayRotation^:^0^,^blockSensor^:^true^,^forceBlock^:^true^}"
)
OLD_ROW = (
    '<a package_name="com.tencent.mobileqq" status="2" func_version="1.5" '
    'use_function="magicwindow" custom_config_body="' + OLD_BODY_CARET + '" />'
)

# Runtime config from old live DB (excludeDevice PAD) + body
OLD_CFG = json.dumps({
  "mode":"1",
  "excludeDevice":"FOLD|PAD",
  "Activities":[
    {"name":"com.tencent.mobileqq.filemanager.fileviewer.FileBrowserActivity","defaultFullScreen":"true"},
    {"name":"com.tencent.mobileqq.filemanager.fileviewer.TroopFileDetailBrowserActivity","defaultFullScreen":"true"},
    {"name":"cooperation.qqfav.QfavPluginProxyActivity$SingleTop","defaultFullScreen":"true"},
    {"name":"cooperation.qqfav.QfavPluginProxyActivity$ImageViewer","defaultFullScreen":"true"},
    {"name":"com.tencent.mobileqq.activity.shortvideo.ShortVideoPlayActivity","defaultFullScreen":"true"},
    {"name":"com.tencent.av.ui.AVActivity","defaultFullScreen":"true"},
    {"name":"com.tencent.av.ui.VideoInviteActivity","defaultFullScreen":"true"}
  ],
  "UX":{"supportRotationUxCompat":"false","isDraggable":"true"}
}, separators=(',',':'))
OLD_BODY = json.dumps({
  "Activities":[{"name":"*","reverseCameraRotation":"10","reverseCameraRotationFront":"9"}],
  "noRelaunchOnResize":"true",
  "adjustDisplayRotation":"0",
  "blockSensor":"true",
  "forceBlock":"true"
}, separators=(',',':'))

xml = open(src_xml, encoding='utf-8').read()
pat = re.compile(r'<a\s+package_name="com\.tencent\.mobileqq"[^/]*/>', re.S)
m = pat.search(xml)
if not m:
    raise SystemExit('QQ magic row not found in product XML')
print('OLD_ROW_SNIP:', m.group(0)[:180])
xml2, n = pat.subn(OLD_ROW, xml, count=1)
if n != 1:
    raise SystemExit(f'replace count={n}')
open(dst_xml,'w',encoding='utf-8',newline='\n').write(xml2)
print('XML_MD5', hashlib.md5(open(dst_xml,'rb').read()).hexdigest())
print('NEW_ROW', OLD_ROW[:200])

# FO: enable status=1 so landscape stays (old package landscape was native; FO=1 helps current port)
fo = open(fo_src, encoding='utf-8').read()
fo_pat = re.compile(r'<o\s+package_name="com\.tencent\.mobileqq"[^/]*/>')
FO_ROW = '<o package_name="com.tencent.mobileqq" status="1" use_function="fullorientation" custom_config_body="{^rao^:^false^,^rotate_cam^:^false^}" />'
m2 = fo_pat.search(fo)
print('FO_OLD', m2.group(0) if m2 else 'MISSING')
if m2:
    fo2, n2 = fo_pat.subn(FO_ROW, fo, count=1)
else:
    # insert before </filter-conf> or end
    fo2 = fo.replace('</filter-conf>', '    '+FO_ROW+'\n</filter-conf>')
    if fo2 == fo:
        fo2 = fo + '\n' + FO_ROW + '\n'
    n2 = 1
open(fo_dst,'w',encoding='utf-8',newline='\n').write(fo2)
print('FO_MD5', hashlib.md5(open(fo_dst,'rb').read()).hexdigest(), 'n', n2)

shutil.copy2(src_db, dst_db)
con = sqlite3.connect(dst_db)
cur = con.cursor()
# magic restore
cur.execute(
  "UPDATE t_config SET status=2, custom_mode=0, config=?, custom_config_body=?, data_sources=1 WHERE package_name='com.tencent.mobileqq' AND use_function='magicwindow'",
  (OLD_CFG, OLD_BODY)
)
print('magic_rows', cur.rowcount)
# FO enable
cur.execute(
  "UPDATE t_config SET status=1, custom_mode=0, custom_config_body=? WHERE package_name='com.tencent.mobileqq' AND use_function='fullorientation'",
  ('{"rao":"false","rotate_cam":"false"}',)
)
print('fo_rows', cur.rowcount)
# if FO missing insert
cur.execute("SELECT count(*) FROM t_config WHERE package_name='com.tencent.mobileqq' AND use_function='fullorientation'")
if cur.fetchone()[0]==0:
    cur.execute("INSERT INTO t_config(package_name,use_function,config,data_sources,status,custom_mode,custom_config_body,func_version,installed) VALUES('com.tencent.mobileqq','fullorientation','',1,1,0,?,?,1)",
                ('{"rao":"false","rotate_cam":"false"}','1.5'))
    print('fo_inserted')
con.commit()
for row in cur.execute("SELECT use_function,status,custom_mode,length(config),substr(custom_config_body,1,80) FROM t_config WHERE package_name='com.tencent.mobileqq'"):
    print('VERIFY', row)
con.close()
print('DB_MD5', hashlib.md5(open(dst_db,'rb').read()).hexdigest())
print('OK_BUILD')
