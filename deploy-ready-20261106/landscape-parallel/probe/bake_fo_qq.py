from pathlib import Path
import re, hashlib, shutil
base = Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe")
src = base / "sys_full_orientation_managed.stock.xml"
dst = base / "sys_full_orientation_managed.qq-fo-v1.xml"
t = src.read_text(encoding="utf-8")

def patch_pkg(text, pkg, body):
    # body uses caret-quotes as OEM format
    pat = re.compile(
        r'(<o package_name="' + re.escape(pkg) + r'" status=")(\d+)(" use_function="fullorientation" custom_config_body=")([^"]*)(" />)'
    )
    m = pat.search(text)
    if not m:
        raise SystemExit(f"no row for {pkg}")
    before = m.group(0)
    after = m.group(1) + "1" + m.group(3) + body + m.group(5)
    print("PKG", pkg)
    print("BEFORE status", m.group(2), "body_len", len(m.group(4)))
    print("AFTER ", after[:180], "...")
    return pat.sub(after, text, count=1)

# Douyin-proven simple FO body (OEM caret JSON)
BODY = "{^rao^:^true^,^rotate_cam^:^false^}"
t2 = patch_pkg(t, "com.tencent.mobileqq", BODY)
# Also bake aweme the same way so Douyin FO survives cloud/DB rebuild (was DB-only interim)
t2 = patch_pkg(t2, "com.ss.android.ugc.aweme", BODY)
dst.write_text(t2, encoding="utf-8", newline="\n")
# verify single replacements
assert t2.count('package_name="com.tencent.mobileqq" status="1"') == 1
assert 'package_name="com.tencent.mobileqq" status="2"' not in t2
assert t2.count('package_name="com.ss.android.ugc.aweme" status="1"') >= 1
md5 = hashlib.md5(dst.read_bytes()).hexdigest()
stock = hashlib.md5(src.read_bytes()).hexdigest()
print("STOCK_MD5", stock)
print("BAKE_MD5", md5)
print("WROTE", dst)
