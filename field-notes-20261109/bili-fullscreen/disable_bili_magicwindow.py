p = r"E:\youxikaifa\work\sys_fantasy_window_managed.xml"
lines = open(p, encoding="utf-8").read().splitlines()
out = []
removed = 0
for l in lines:
    if 'package_name="tv.danmaku.bili"' in l:
        removed += 1
        continue
    out.append(l)
s = "\n".join(out) + "\n"
assert removed == 1, removed
oldv = "<version>20253027</version>"
newv = "<version>20253028</version>"
assert s.count(oldv) == 1, s.count(oldv)
s = s.replace(oldv, newv, 1)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("removed bili magicwindow entry:", removed, "version 20253028")
