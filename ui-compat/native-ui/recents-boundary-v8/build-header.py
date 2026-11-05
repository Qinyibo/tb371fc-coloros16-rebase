from pathlib import Path
import hashlib,json,re,subprocess,sys,zipfile
r=Path.cwd();w=r/'ui-compat/native-ui/recents-boundary-v8';build=w/'build';build.mkdir(exist_ok=True)
sys.path.insert(0,str(r/'ui-compat/native-ui'))
from apk_container import replace_dex
apk=r/'ui-compat/native-ui/tablet-viewport-v6r2/build/OplusLauncher.apk';raw=apk.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='c2d75443b1778e274b736cd1c46814c27e276ef82a7450aa5a3002416fe4d6cd'
cp=';'.join(str(p) for p in Path('C:/android-sdk/cmdline-tools/latest/lib').rglob('*.jar') if any(t in str(p).lower() for t in ['smali','guava','failureaccess']))
java='C:/Program Files/Java/jdk-21/bin/java.exe'
subprocess.run(['C:/Program Files/Java/jdk-21/bin/javac.exe','-cp',cp,'-d',str(build),str(w/'HeaderButtonPatch.java')],check=True,capture_output=True,timeout=30)
changes=0
with zipfile.ZipFile(apk) as z:
 for name in z.namelist():
  if not re.fullmatch(r'classes\d*\.dex',name):continue
  p=build/name;p.write_bytes(z.read(name));out=build/(name+'.patched')
  x=subprocess.run([java,'-cp',str(build)+';'+cp,'HeaderButtonPatch',str(p),str(out)],capture_output=True,timeout=45)
  assert x.returncode==0,(x.stdout+x.stderr).decode(errors='replace')
  n=int(re.search(r'CHANGES (\d+)',x.stdout.decode())[1]);changes+=n
  if n:raw=replace_dex(raw,name,out.read_bytes());print('header method changed in',name,flush=True)
 assert changes==1
 out=build/'OplusLauncher.apk';out.write_bytes(raw)
 with zipfile.ZipFile(out) as new:
  assert z.namelist()==new.namelist() and new.testzip() is None
  assert all(z.read(n)==new.read(n) for n in z.namelist() if not re.fullmatch(r'classes\d*\.dex',n))
x=subprocess.run([java,'-cp',str(r/'ui-compat/native-ui/stack-v4/compare-classes')+';'+cp,'CompareApkDex',str(apk),str(out)],check=True,capture_output=True,timeout=90)
(build/'diff.txt').write_bytes(x.stdout+x.stderr)
diff=x.stdout.decode();assert 'REMOVED 0' in diff and 'ADDED 0' in diff and 'CHANGED 1' in diff,diff[-2000:]
(w/'header-build.json').write_text(json.dumps({'source_apk_sha256':hashlib.sha256(apk.read_bytes()).hexdigest(),'apk_sha256':hashlib.sha256(raw).hexdigest(),'changed_existing_methods':1,'new_methods_classes':0,'non_dex_entries_identical':True,'scope':'At native header binding owner, hide the standalone split button only in native stacked recents. Other native layouts and split-screen capability unchanged.','original_oem_cryptographic_signature_valid':False,'integrated':False,'physical_verified':False,'boundary_bug_fixed':False},indent=2)+'\n')
print(diff[-1800:],flush=True)
