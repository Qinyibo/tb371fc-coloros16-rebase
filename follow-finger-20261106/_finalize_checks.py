import zipfile, pathlib, hashlib, time
z=pathlib.Path(r'D:/TB371FC-release/clean-rebase-20261104/deploy-ready-20261106/dynframe-144-trial/tb371fc_dynframe_144-trial.zip')
with zipfile.ZipFile(z) as zf:
  print('namelist:')
  for n in zf.namelist():
    info=zf.getinfo(n)
    print(n, info.file_size)
  data=zf.read('my_product/etc/sys_dynamic_frame_config.xml')
  print('xml_md5', hashlib.md5(data).hexdigest(), 'len', len(data))
  print('count120', data.count(b'targetFramerate="120"'), 'count144', data.count(b'targetFramerate="144"'))

flu=pathlib.Path(r'D:/TB371FC-release/clean-rebase-20261104/follow-finger-20261106/FLUENCY-144-NEXT.md')
t=flu.read_text(encoding='utf-8')
addon = """

## Fresh warm metrics (2026-11-06 14:42 Asia/Hong_Kong)
Dir: `warm-switch-gfx-20261106-144225`
Same PIDs throughout (no cold): mm=9415 aweme=20485 luna=9376
| App | frames | janky% | High input latency | p90 |
|-----|--------|---------|--------------------|-----|
| WeChat | 430 | 16.74 | **669** | 23ms |
| Douyin | 311 | 29.26 | **379** | 46ms |
| Luna | 411 | 32.60 | **504** | 38ms |
PickRate remained 144 across cycles (smsum dumps).
"""
if 'warm-switch-gfx-20261106-144225' not in t:
  flu.write_text(t+addon, encoding='utf-8')
  print('fluency updated')
else:
  print('fluency already has fresh metrics')

bake=pathlib.Path(r'D:/TB371FC-release/clean-rebase-20261104/deploy-ready-20261106/display-refresh-system-v4/bake-in/BAKE-IN.md')
bt=bake.read_text(encoding='utf-8')
bt2=bt.replace('../magisk-module/', '../product-config/magisk-module/')
if bt2!=bt:
  bake.write_text(bt2, encoding='utf-8')
  print('BAKE-IN path fixed')
else:
  print('BAKE-IN path unchanged')

ring=pathlib.Path(r'D:/TB371FC-release/clean-rebase-20261104/blackscreen-ring')
cur=(ring/'CURRENT.txt').read_text(encoding='utf-8', errors='ignore')
print('CURRENT', cur.strip())
latest=max(ring.glob('ring-*.log'), key=lambda p: p.stat().st_mtime)
st=latest.stat()
print('latest', latest.name, 'size', st.st_size, 'mtime', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.st_mtime)))

# list deliverables
for p in [
  r'D:/TB371FC-release/clean-rebase-20261104/deploy-ready-20261106/display-refresh-system-v4/ROM-BAKE-IN-HANDOFF.md',
  r'D:/TB371FC-release/clean-rebase-20261104/follow-finger-20261106/FLUENCY-144-NEXT.md',
  r'D:/TB371FC-release/clean-rebase-20261104/deploy-ready-20261106/dynframe-144-trial/TRIAL.md',
  r'D:/TB371FC-release/clean-rebase-20261104/deploy-ready-20261106/dynframe-144-trial/tb371fc_dynframe_144-trial.zip',
]:
  pp=pathlib.Path(p)
  print('DELIVER', pp.exists(), pp, pp.stat().st_size if pp.exists() else 0)
