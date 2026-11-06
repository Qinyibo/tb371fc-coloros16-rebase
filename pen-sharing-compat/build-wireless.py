from pathlib import Path
import subprocess,json,zipfile,re,sys,hashlib
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--output',default='build');args=ap.parse_args()
w=Path(__file__).resolve().parent;p=w/'PenDexPatchV3.java';s=p.read_text();assert 'Lcom/oplus/wirelesssettings/utils/q;' in s
c=json.loads((w/'dex-classpath.json').read_text());j=Path(c['java']);b=w/args.output;cp=c['cp'];subprocess.run([str(j/'javac.exe'),'-cp',cp,'-d',str(b),str(p)],capture_output=True,check=True)
sys.path.insert(0,str(w.parent/'ui-compat/native-ui'));from apk_container import replace_dex,append_dex
source=w/'WirelessSettings-current.apk';original=source.read_bytes();assert hashlib.sha256(original).hexdigest()=='53896e3b43b146e58a257553f7b73a1c00ce616909b2f09e16388f79cd09a14f';raw=original;stage=b/'WirelessSettings-current.apk';stage.mkdir(exist_ok=True);count=0;edits=[];changed=[]
with zipfile.ZipFile(source) as z:
 names=[n for n in z.namelist() if re.fullmatch(r'classes\d*\.dex',n)]
 for n in names:
  inp=stage/n;inp.write_bytes(z.read(n));out=stage/(n+'.patched');x=subprocess.run([str(j/'java.exe'),'-cp',str(b)+';'+cp,'PenDexPatchV3',str(inp),str(out),'ws'],capture_output=True,check=True,timeout=30);(stage/(n+'.log')).write_bytes(x.stdout+x.stderr)
  m=re.search(rb'PATCHED (\d+)',x.stdout)
  if m:count+=int(m[1]);raw=replace_dex(raw,n,out.read_bytes());changed.append(n);edits+=x.stdout.decode(errors='replace').splitlines()
 assert count==1,count
 last=max(1 if n=='classes.dex' else int(re.search(r'\d+',n)[0]) for n in names);extra=f'classes{last+1}.dex';raw=append_dex(raw,extra,(b/'pen-dex/classes.dex').read_bytes());target=stage/'WirelessSettings-pen-v1.apk';target.write_bytes(raw)
 with zipfile.ZipFile(target) as dz:
  assert dz.testzip() is None
  assert all(z.read(n)==dz.read(n) for n in z.namelist() if n not in changed)
p=b/'pen-build-result.json';d=json.loads(p.read_text());d[source.name]={'input_sha256':hashlib.sha256(original).hexdigest(),'output':target.relative_to(w).as_posix(),'output_sha256':hashlib.sha256(raw).hexdigest(),'modified_methods':count,'edits':edits,'added_dex':extra,'unmodified_entry_contents_preserved':True,'device_verified':False,'scope':'Add real Lenovo pen name classification; stock OEM names and server list fallback retained. Classification does not assert GATT connection.'};d['limits']['wireless_settings_ui_pending']=False;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('WIRELESS_SETTINGS_ONE_PEN_CLASSIFIER_BUILT',count)
