from pathlib import Path
import subprocess,zipfile,re,hashlib,json,sys,struct,copy,argparse
r=Path(__file__).resolve().parent;root=r.parent;sys.path.insert(0,str(root/'ui-compat/native-ui'))
from apk_container import replace_dex,append_dex
ap=argparse.ArgumentParser();ap.add_argument('--output',default='build');args=ap.parse_args();b=r/args.output;b.mkdir(exist_ok=True);cfg=json.loads((r/'dex-classpath.json').read_text());cp=cfg['cp'];j=Path(cfg['java']);sdk=Path('C:/android-sdk');android=sdk/'platforms/android-36/android.jar';d8=sdk/'build-tools/36.0.0/lib/d8.jar'
def run(args,name):
 p=subprocess.run(list(map(str,args)),capture_output=True,timeout=100);(b/(name+'.log')).write_bytes(p.stdout+p.stderr)
 if p.returncode:raise RuntimeError(name+' '+p.stderr.decode(errors='replace')[-1800:])
 return p.stdout.decode(errors='replace')
def jar_classes(folder,target):
 with zipfile.ZipFile(target,'w') as z:
  for p in folder.rglob('*.class'):z.write(p,p.relative_to(folder).as_posix())
def compile_helper(name,source,classpath):
 c=b/(name+'-classes');c.mkdir(exist_ok=True);run([j/'javac.exe','--release','8','-cp',classpath,'-d',c,*source],name+'-javac');jar=b/(name+'.jar');jar_classes(c,jar);dex=b/(name+'-dex');dex.mkdir(exist_ok=True)
 run([j/'java.exe','-cp',d8,'com.android.tools.r8.D8','--min-api','36','--lib',android,'--output',dex,jar],name+'-d8');return (dex/'classes.dex').read_bytes()
run([j/'javac.exe','-cp',cp,'-d',b,r/'PenDexPatchV3.java',r/'ServicesPenPatch.java'],'compile-patchers')
helper=compile_helper('pen',list((r/'src').rglob('*.java')),android)
stubs=b/'stub-classes';stubs.mkdir(exist_ok=True);run([j/'javac.exe','--release','8','-cp',android,'-d',stubs,*list((r/'stubs').rglob('*.java'))],'compile-system-stubs');stubjar=b/'stubs.jar';jar_classes(stubs,stubjar)
system=compile_helper('pen-system',list((r/'system-src').rglob('*.java')),str(android)+';'+str(stubjar))
# Verify actual pre-rebase/current linkage before producing any preload.
contracts=(r/'IPeManager-current.apk.contracts-v2.txt').read_text(errors='replace')
for member in ['ble/g;->p()Landroid/content/Context;','ble/g;->r()Landroid/bluetooth/BluetoothGatt;','ble/g;->w(Landroid/bluetooth/BluetoothDevice;)V','ble/l0;->H0(I)V','ble/l0;->K:I','ble/l0;->L:I','ble/l0;->M:Ljava/lang/String;','ble/l0;->T0:Lcom/oplus/ipemanager/pencilpanel/IPencilPanelCallback;','ble/l0;->Z0:Lcom/oplus/ipemanager/pencilpanel/IPencilPanelCallback;','util/v;->W(Landroid/content/Context;Ljava/lang/String;)Z','Lb2/b;->a(ILjava/lang/String;)V','Lb2/b;->b(Ljava/lang/String;Ljava/lang/String;)V','Lv1/b;->i(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)V','Lv1/b;->g(Landroid/content/Context;ILjava/lang/String;)V']:
 assert member in contracts,member
results={}
for name,tool,mode,expected,extra in [('IPeManager-current.apk','PenDexPatchV3','ipe',17,helper),('services-current.jar','ServicesPenPatch',None,2,system)]:
 source=r/name;original=source.read_bytes();raw=original;stage=b/name;stage.mkdir(exist_ok=True);changes={};count=0;edits=[]
 if name.startswith('IPe'):assert hashlib.sha256(original).hexdigest()=='4caa374981f03080a7e887cda1baadd95a2c1edb5e283a8847ebedfb563ddbf7'
 with zipfile.ZipFile(source) as z:
  dexnames=[n for n in z.namelist() if re.fullmatch(r'classes\d*\.dex',n)]
  for n in dexnames:
   inp=stage/n;inp.write_bytes(z.read(n));dest=stage/(n+'.patched')
   args=[j/'java.exe','-cp',str(b)+';'+cp,tool,inp,dest]+([mode] if mode else [])
   log=run(args,name+'-'+n);m=re.search(r'PATCHED (\d+)',log)
   if m and int(m[1]):
    count+=int(m[1]);changes[n]=dest.read_bytes();edits+=log.strip().splitlines()
  assert count==expected,(name,count,expected)
  last=max(1 if n=='classes.dex' else int(re.search(r'\d+',n)[0]) for n in dexnames);extra_name=f'classes{last+1}.dex'
  if name.endswith('.apk'):
   for n,v in changes.items():raw=replace_dex(raw,n,v)
   raw=append_dex(raw,extra_name,extra)
   target=stage/'IPeManager-pen-v1.apk';target.write_bytes(raw)
  else:
   target=stage/'services-pen-v1.jar'
   with zipfile.ZipFile(target,'w') as dz:
    for e in z.infolist():dz.writestr(copy.copy(e),changes.get(e.filename,z.read(e.filename)))
    dz.writestr(extra_name,extra)
  with zipfile.ZipFile(target) as dz:
   assert dz.testzip() is None
   assert all(z.read(n)==dz.read(n) for n in z.namelist() if n not in changes)
  results[name]={'input_sha256':hashlib.sha256(original).hexdigest(),'output':target.relative_to(r).as_posix(),'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'modified_methods':count,'edits':edits,'added_dex':extra_name,'unmodified_entry_contents_preserved':True,'device_verified':False}
results['limits']={'preload_only':True,'oem_signature_valid_after_apk_modification':False,'scope':'Compiled trusted-preload candidate; original certificate identity retained as in existing ROM build. No APK verification bypass or runtime mount introduced. Not an ordinary signed APK update.','no_pen_hardware_acceptance':True,'no_system_server_restart_performed':True,'wireless_settings_ui_pending':True}
(b/'pen-build-result.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:{'methods':v['modified_methods'],'output':v['output']} for k,v in results.items() if k!='limits'},ensure_ascii=False),flush=True)
