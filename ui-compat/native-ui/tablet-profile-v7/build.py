"""Adapt the existing tablet RRO profile; adds no runtime code or overlay layer."""
from pathlib import Path
import hashlib,json,re,struct,subprocess,sys,zipfile
root=Path.cwd();w=root/'ui-compat/native-ui/tablet-profile-v7'
sys.path.insert(0,str(root/'ui-compat/native-ui'))
from apk_container import replace_dex
source=w/'LauncherResourceOverlay.before.apk';raw=source.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='902c5fb7076733b03e04dbeaa98829a5f172de081f326459e0e71348342fe7d5'
with zipfile.ZipFile(source) as z: original=z.read('resources.arsc')
s=bytearray(original)
def chunks(a,b):
 while a<b:
  t,h,n=struct.unpack_from('<HHI',s,a);assert h>=8 and n>=h and a+n<=b
  yield a,t,h,n;a+=n
changes=[]
assert struct.unpack_from('<HHI',s,0)==(2,12,len(s))
for o,t,h,n in chunks(12,len(s)):
 if t!=0x200: continue
 assert struct.unpack_from('<I',s,o+8)[0]==0x7f
 for q,t,h,n in chunks(o+h,o+n):
  if t!=0x201 or s[q+8]!=6:continue
  assert s[q+9]==0,'Unexpected sparse or compact resource table'
  count,start=struct.unpack_from('<II',s,q+12)
  assert count>0x11
  e=struct.unpack_from('<I',s,q+h+0x11*4)[0]
  if e==0xffffffff:continue
  pos=q+start+e;entry_size,flags,key=struct.unpack_from('<HHI',s,pos)
  assert entry_size==8 and flags==0
  value=pos+entry_size
  size,reserved,kind,data=struct.unpack_from('<HBBI',s,value)
  assert (size,reserved,kind)==(8,0,16)
  orientation=s[q+32]
  if orientation==1:
   assert data==133
   struct.pack_into('<I',s,value+4,72)
   changes.append({'resource':'integer/oplusLayoutWorkspacePaddingHorBigScreenDp','configuration':'port','before':133,'after':72,'resource_id':'0x7f060011'})
  elif orientation==2:assert data==106
  else:raise AssertionError('Unexpected orientation for workspace margin')
assert len(changes)==1
changed=[i for i,(a,b) in enumerate(zip(original,s)) if a!=b]
assert len(changed)==1,changed
out=w/'unsigned.apk';out.write_bytes(replace_dex(raw,'resources.arsc',bytes(s)))
with zipfile.ZipFile(source) as a,zipfile.ZipFile(out) as b:
 assert a.namelist()==b.namelist() and b.testzip() is None
 assert all(a.read(n)==b.read(n) for n in a.namelist() if n!='resources.arsc')
aapt='C:/android-sdk/build-tools/36.0.0/aapt2.exe'
r=subprocess.run([aapt,'dump','resources',str(out)],capture_output=True,check=True,timeout=20)
(w/'resources.after.txt').write_bytes(r.stdout)
before=(w/'resources.before.txt').read_text(encoding='utf-8-sig').replace('\r','')
after=r.stdout.decode().replace('\r','')
expected=before.replace('integer/oplusLayoutWorkspacePaddingHorBigScreenDp\n      (port) 133','integer/oplusLayoutWorkspacePaddingHorBigScreenDp\n      (port) 72')
assert after==expected and after!=before,'Unexpected resource dump difference'
(w/'resource-diff.json').write_text(json.dumps({'source_sha256':'902c5fb7076733b03e04dbeaa98829a5f172de081f326459e0e71348342fe7d5','changes':changes,'all_other_resources_and_payloads_identical':True,'new_runtime_code':False,'extra_overlay_layer':False,'physical_verified':False},indent=2)+'\n')
print('EXISTING_TABLET_RRO_SINGLE_PORTRAIT_RESOURCE_CHANGE_PASS')
