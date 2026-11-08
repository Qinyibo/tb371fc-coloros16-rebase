import sqlite3, shutil
probe=r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe"
src=probe+r"\fw-after-native.db"
dst=probe+r"\fw-native-douyin-v2.db"
shutil.copy2(src,dst)
c=sqlite3.connect(dst)
# Simplify fullorientation body like enabled apps (luna-style), keep status=1
# Also try rao true - some OEMs use rao for rotate-as-override
body='{"rao":"true","rotate_cam":"false"}'
c.execute("update t_config set status=1, custom_config_body=?, config=? where package_name='com.ss.android.ugc.aweme' and use_function='fullorientation'", (body, '{"rao":"true","rotate_cam":"false"}'))
# ensure magic still off
c.execute("update t_config set status=2, config=? where package_name='com.ss.android.ugc.aweme' and use_function='magicwindow'", ('{"mode":"1","excludeDevice":"PAD"}',))
c.commit()
print(c.execute("select use_function,status,config,custom_config_body from t_config where package_name='com.ss.android.ugc.aweme' and use_function in ('fullorientation','magicwindow')").fetchall())
c.close()
print("wrote", dst)
