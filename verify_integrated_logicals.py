import hashlib,json,pathlib,sys
r=pathlib.Path(sys.argv[1]);out=r/'integrated-logicals'
exec((r/'verify_base.py').read_text().split("for name in ['system','system_ext']:")[0].replace('results={}','results={}'))
root='system/framework/'
drop={root+x for x in ('oplus-services.jar.fsv_meta','oplus-services.jar.prof','oplus-services.jar.prof.fsv_meta')}
for ext in ('art','odex','vdex'):
 for side in ('','.fsv_meta'):
  drop.add(root+'oat/arm64/oplus-services.ocomp.'+ext+side)
jar=root+'oplus-services.jar'
apex='apex/com.android.vndk.v30.apex'
policy='etc/selinux/system_ext_sepolicy.cil'
sig='etc/selinux/system_ext_sepolicy_and_mapping.sha256'
changes={
 'system':(set(),drop,{jar}),
 'system_ext':({apex},set(),{policy,sig}),
 'product':({'lost+found'},set(),set()),
}
for n in changes:
 before=inventory(r/'mounts/product' if n=='product' else out/('baseline-'+n))
 after=inventory(out/('verify-'+n))
 add,remove,modify=changes[n]
 assert after.keys()-before.keys()==add,(n,after.keys()-before.keys())
 assert before.keys()-after.keys()==remove,(n,before.keys()-after.keys())
 d={p for p in before.keys()&after.keys() if before[p]!=after[p]}
 assert d==modify,(n,d,[(p,before[p],after[p]) for p in sorted(d-modify)[:2]])
 for p in modify:
  assert {k:v for k,v in before[p].items() if k not in ('size','sha256')}=={k:v for k,v in after[p].items() if k not in ('size','sha256')},p
 if n=='system':
  assert after[jar]['sha256']=='25bbb67269b54965517d9d7fd9306dd0ba324f5ed89e7d7ad14960ab99e7c335'
 if n=='system_ext':
  expected=json.loads((r/'apex-inputs/source.json').read_text())[1]['sha256']
  assert after[apex]['sha256']==expected
  assert {k:v for k,v in after[apex].items() if k not in ('size','sha256')}=={k:v for k,v in before['apex/com.android.compos.apex'].items() if k not in ('size','sha256')}
  pp=out/'verify-system_ext'/policy
  donor=r/'mounts/system_ext'/policy
  assert pp.read_bytes()==donor.read_bytes()+b'\n'+(r/'policy-check/legacy-vendor-types.cil').read_bytes()
  mapping=(out/'verify-system_ext/etc/selinux/mapping/202504.cil').read_bytes()
  assert (out/'verify-system_ext'/sig).read_text().strip()==hashlib.sha256(pp.read_bytes()+mapping).hexdigest()
 if n=='product':
  assert not list((out/'verify-product/lost+found').iterdir())
 results[n]=dict(entries=len(after),add=sorted(add),remove=sorted(remove),modify=sorted(modify))
(out/'tree-verification.json').write_text(json.dumps(results,indent=2)+'\n')
print('INTEGRATED_TREE_EXACT_DELTA_PASS')
