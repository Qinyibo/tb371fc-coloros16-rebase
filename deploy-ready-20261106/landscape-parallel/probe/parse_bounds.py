import re
t=open(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\probe\qq-login-ui2.xml",encoding="utf-8").read()
for m in re.finditer(r"<node\b[^>]*>", t):
    s=m.group(0)
    tx=re.search(r'text="([^"]*)"', s)
    bd=re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', s)
    if tx and bd and tx.group(1):
        print(tx.group(1), bd.groups())
