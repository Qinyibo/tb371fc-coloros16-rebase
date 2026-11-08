import re
p=r'D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\ui-deploy-20261106\verify\parallel-ui-attempt2.xml'
t=open(p,encoding='utf-8',errors='ignore').read()
print('len',len(t))
# all texts
texts=re.findall(r'text="([^"]+)"', t)
print('texts unique sample:')
seen=[]
for x in texts:
  if x and x not in seen:
    seen.append(x)
print('\n'.join(seen[:60]))
switches=re.findall(r'class="android.widget.Switch"[^>]*checked="([^"]+)"', t)
print('switches', switches)
titles=re.findall(r'resource-id="android:id/title"[^>]*text="([^"]*)"|text="([^"]*)"[^>]*resource-id="android:id/title"', t)
print('titles', titles)
