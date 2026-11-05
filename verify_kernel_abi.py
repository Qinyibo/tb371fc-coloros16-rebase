import json,pathlib,subprocess,sys
r,old,k=map(pathlib.Path,sys.argv[1:])
def export(path):
 entries={}
 for line in path.read_text().splitlines():
  crc,sym,*_=line.split()
  if sym in entries:assert entries[sym]==int(crc,16),(path,sym)
  entries[sym]=int(crc,16)
 return entries
a=export(old/'Module.symvers');b=export(k/'Module.symvers')
removed=sorted(a.keys()-b.keys())
changed={s:[hex(a[s]),hex(b[s])] for s in a.keys()&b.keys() if a[s]!=b[s]}
paths=[p for n in ('tb-vendor','tb-odm') for p in sorted((r/'mounts'/n).glob('**/lib/modules/**/*.ko'))]
providers={}
for p in paths:
 for line in subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',p],text=True).splitlines():
  parts=line.split()
  if len(parts)==3 and parts[1]=='A' and parts[2].startswith('__crc_'):
   providers.setdefault(parts[2][6:],[]).append((int(parts[0],16),p.name))
mods=[]
for p in paths:
 req=[]
 for line in subprocess.check_output(['modprobe','--dump-modversions',p],text=True).splitlines():
  crc,sym=line.split();req.append((int(crc,16),sym))
 assert req,p
 abi=[]; inter_module={}
 for crc,sym in req:
  if a.get(sym)==crc and b.get(sym)==crc:continue
  refs=sorted({name for c,name in providers.get(sym,[]) if name!=p.name and c==crc})
  if sym not in a and b.get(sym,crc)==crc and len(refs)==1:
   inter_module[sym]=refs[0];continue
  abi.append(dict(symbol=sym,module=hex(crc),original=hex(a[sym]) if sym in a else None,new=hex(b[sym]) if sym in b else None))
 mods.append(dict(name=p.name,version=subprocess.check_output(['modinfo','-F','vermagic',p],text=True).strip(),references=len(req),inter_module=inter_module,nonmatching=abi))
receipt=dict(scope='All previous kernel symbol CRCs and actual retained vendor module references, no module load claim',original_exports=len(a),new_exports=len(b),removed=removed,changed=changed,modules=mods)
(k/'abi-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
assert len(mods)==9 and not removed and not changed and not any(m['nonmatching'] for m in mods), 'see abi-verification.json'
print('R107_EXPORTED_ABI_AND_9_VENDOR_MODULE_CRCS_PASS')
