import re, pathlib
p=pathlib.Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\qq-login-ui.xml")
t=p.read_text(encoding='utf-8', errors='replace')
texts=re.findall(r'text="([^"]+)"', t)
print("TEXTS:")
for x in texts:
    if x.strip():
        print(" -", x)
print("\nCONTENT_DESC:")
for x in re.findall(r'content-desc="([^"]+)"', t):
    if x.strip(): print(" -", x)
print("\nRESOURCE_IDS:")
for x in re.findall(r'resource-id="([^"]+)"', t):
    if x.strip(): print(" -", x)
