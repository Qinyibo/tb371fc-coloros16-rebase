import hashlib,json,pathlib,struct
r=pathlib.Path(__file__).resolve().parent
def cpio(path):
 b=path.read_bytes();p=0;out={}
 while p<len(b):
  assert b[p:p+6] in (b'070701',b'070702')
  v=[int(b[p+6+i*8:p+14+i*8],16) for i in range(13)];p+=110;n=b[p:p+v[11]-1].decode();p=(p+v[11]+3)&~3;d=b[p:p+v[6]];p=(p+v[6]+3)&~3
  if n=='TRAILER!!!':break
  out[n]=(v[1],v[2],v[3],d)
 return out
before=cpio(r/'boot-audit/ramdisk.cpio');after=cpio(r/'boot-cleanbase/readback/ramdisk.cpio')
removed={'overlay.d/r93-init.rc',*[f'overlay.d/sbin/{n}' for n in ['r91-SHA256SUMS','r91-apply.sh','r93-apply.sh','r93-health.sh','r93-magisk-bin.tgz','r93-manager.apk','r93-manager.sh','r93-seed-base.sh','r93-seed.sh']]}
assert before.keys()-after.keys()==removed and not after.keys()-before.keys()
assert all(before[n]==after[n] for n in after)
orig=(r/'tb-inputs/boot-r107.img').read_bytes();new=(r/'boot-cleanbase/boot-r107-cleanbase.img').read_bytes()
page=struct.unpack_from('<I',orig,36)[0];a=bytearray(orig[:page]);b=bytearray(new[:page])
for start,end in [(16,20),(576,608),(1636,1644)]:a[start:end]=b'\0'*(end-start);b[start:end]=b'\0'*(end-start)
assert a==b,'unexpected boot header change'
result=dict(scope='Offline boot component only; no device boot or full-ROM claim',bytes=len(new),sha256=hashlib.sha256(new).hexdigest(),kernel_and_dtb_preserved=True,retained_cpio_entries_identical=True,retained_entries=len(after),removed=sorted(removed),header_invariants_pass=True,tb_fstab_preserved=True,magisk_core_preserved=True,device_boot_tested=False)
(r/'boot-cleanbase/build-result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
