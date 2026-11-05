import json,os,pathlib,shutil,sys
r=pathlib.Path(__file__).resolve().parent
base=pathlib.Path('D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE')
j=json.loads((r/'candidate-offline.json').read_text(encoding='utf-8'))
v=j['vbmeta_reference']; rollback=r/'rollback-current-physical'
def stage(name,images):
 out=r/name; out.mkdir(exist_ok=False)
 for n in ('scripts','images','tools'): (out/n).mkdir()
 script=base/'scripts/Invoke-R91-Clean.ps1'
 shutil.copyfile(script,out/'scripts'/script.name)
 for p in (base/'tools').iterdir():
  if p.is_file():shutil.copyfile(p,out/'tools'/p.name)
 rows=[]
 for target,(p,b,h) in images.items():
  assert p.stat().st_size==b and p.drive.upper()=='D:' and len(h)==64,(p,b,h)
  dest=out/'images'/p.name;os.link(p,dest)
  assert os.path.samefile(p,dest)
  rows.append(dict(name=target,path=f'images/{dest.name}',bytes=b,sha256=h))
 (out/'manifest.json').write_text(json.dumps(dict(format='tb371fc-r94-rom-v1',state='OFFLINE_VERIFIED_DEVICE_PENDING',product='spinel',slot='a',images=rows),indent=2)+'\n')
 print('STAGED',name,flush=True)
if sys.argv[1]=='network':
    base_result=json.loads((r/'integrated-logicals/super-result.json').read_text())
    result=json.loads((r/'integrated-network/super-result.json').read_text())
    tree=json.loads((r/'integrated-network/tree-verification.json').read_text())
    apex=json.loads((r/'bpf-compat/rebuilt-tethering/result.json').read_text())
    assert tree['only_delta']=='system/apex/com.android.tethering.apex' and tree['metadata_unchanged']
    assert (tree['old_sha256'],tree['new_sha256'])==(apex['official_sha256'],apex['sha256'])
    assert result['logical_partitions'].keys()==base_result['logical_partitions'].keys()
    assert {n for n,vv in result['logical_partitions'].items() if vv!=base_result['logical_partitions'][n]}=={'system_a'}
    vm=(r/'bpf-compat/tethering-vm/serial.log').read_text()
    assert all(t in vm for t in ('DM_VERITY_READY','LOCALNET_COMPLETE cases=24 failed=0','REALUID_COMPLETE cases=10 failed=0','TETHERING_VM_RESULT errors=0'))
    q=json.loads((rollback/'receipt.json').read_text())
    rb=json.loads((r/'flash-rollback/manifest.json').read_text())
    assert q['slot']=='_a' and q['serial']=='REPLACE_WITH_DEVICE_SERIAL' and q['images']['super']['sha256']==rb['images'][0]['sha256']
    stage('flash-network-candidate',dict(
        super=(r/'integrated-network/super-cleanbase-network-OFFLINE.img',result['bytes'],result['sha256']),
        boot=(r/j['boot']['path'],j['boot']['bytes'],j['boot']['sha256']),
        vbmeta=(pathlib.Path(v['vbmeta']),65536,v['vbmeta_sha256']),
        vbmeta_system=(pathlib.Path(v['vbmeta_system']),65536,v['vbmeta_system_sha256'])))
elif sys.argv[1]=='rollback':
 q=json.loads((rollback/'receipt.json').read_text())
 assert q['slot']=='_a' and q['serial']=='REPLACE_WITH_DEVICE_SERIAL'
 stage('flash-rollback', {n:(rollback/q['images'][k]['path'],q['images'][k]['bytes'],q['images'][k]['sha256']) for n,k in dict(super='super',boot='boot_a',vbmeta='vbmeta_a',vbmeta_system='vbmeta_system_a').items()})
else:raise ValueError(sys.argv[1])
