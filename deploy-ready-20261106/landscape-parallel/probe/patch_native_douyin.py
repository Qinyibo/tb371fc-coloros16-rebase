import sqlite3, shutil, os, time, json
probe = r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe"
src = os.path.join(probe, "fw-live.db")
# Work on a copy
dst = os.path.join(probe, "fw-native-douyin.db")
shutil.copy2(src, dst)
# Also keep pre-native backup name
bak2 = os.path.join(probe, "fantasywindow.before-native-20261106.db")
shutil.copy2(src, bak2)

c = sqlite3.connect(dst)
# Show before
print("BEFORE:")
for r in c.execute("select use_function,status,config,substr(custom_config_body,1,120) from t_config where package_name='com.ss.android.ugc.aweme'"):
    print(r)

# 1) Revert magicwindow to OEM PAD-exclude (status=2)
# Prefer restoring from original bak if available
bak = os.path.join(probe, "fantasywindow.db.bak")
magic_config = '{"mode":"1","excludeDevice":"PAD"}'
magic_body = None
if os.path.exists(bak):
    b = sqlite3.connect(bak)
    row = b.execute("select status,config,custom_config_body from t_config where package_name='com.ss.android.ugc.aweme' and use_function='magicwindow'").fetchone()
    print("BAK magic row:", row[0] if row else None, (row[1][:80] if row and row[1] else None))
    if row:
        magic_status, magic_config, magic_body = row[0], row[1], row[2]
    b.close()
else:
    magic_status = 2

c.execute("update t_config set status=?, config=? where package_name='com.ss.android.ugc.aweme' and use_function='magicwindow'",
          (magic_status if 'magic_status' in dir() else 2, magic_config))
# if we got body from bak, restore it too
if magic_body is not None:
    c.execute("update t_config set custom_config_body=? where package_name='com.ss.android.ugc.aweme' and use_function='magicwindow'", (magic_body,))

# 2) Enable fullorientation status=1 (native landscape lever)
# Keep existing custom_config_body (activity exceptions), set status=1 and a simple config if empty
row = c.execute("select status,config,custom_config_body from t_config where package_name='com.ss.android.ugc.aweme' and use_function='fullorientation'").fetchone()
print("fullorient before:", row[0], row[1], (row[2][:100] if row[2] else None))
# status=1 means enabled for full orientation policy
# Use config similar to luna (enabled apps often have empty config and body with rao/rotate_cam)
c.execute("update t_config set status=1 where package_name='com.ss.android.ugc.aweme' and use_function='fullorientation'")

c.commit()
print("AFTER:")
for r in c.execute("select use_function,status,config,substr(custom_config_body,1,120) from t_config where package_name='com.ss.android.ugc.aweme'"):
    print(r)
c.close()
print("WROTE", dst)
