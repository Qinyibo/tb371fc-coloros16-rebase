import re, pathlib
root=pathlib.Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\qq-parallel-deep-20261106")
xml_path=root/"payload"/"sys_fantasy_window_managed.qq-v2.xml"
body=(root/"payload"/"qq-magic-v2.caret.txt").read_text(encoding="utf-8").strip()
text=xml_path.read_text(encoding="utf-8")
pat=re.compile(r'<a package_name="com\.tencent\.mobileqq" status="[^"]*" func_version="[^"]*" use_function="magicwindow" custom_config_body="[^"]*"\s*/>')
repl=f'<a package_name="com.tencent.mobileqq" status="1" func_version="1.5" use_function="magicwindow" custom_config_body="{body}" />'
new,n=pat.subn(repl,text,count=1)
if n!=1:
    raise SystemExit(f"replace count={n}")
xml_path.write_text(new,encoding="utf-8")
print("patched ok", xml_path.stat().st_size)
print("body sample", body[:180])
