from pathlib import Path
import hashlib,json,subprocess,zipfile
r=Path.cwd();w=r/'ui-compat/native-ui/identity-radio-v4';build=w/'build';build.mkdir(exist_ok=True)
cp=';'.join(str(p) for p in Path('C:/android-sdk/cmdline-tools/latest/lib').rglob('*.jar') if any(t in str(p).lower() for t in ['smali','guava','failureaccess']))
java='C:/Program Files/Java/jdk-21/bin/java.exe'
x=subprocess.run(['C:/Program Files/Java/jdk-21/bin/javac.exe','-cp',cp,'-d',str(build),str(w/'OptionalVirtualRadioPatch.java')],capture_output=True,timeout=30);assert x.returncode==0,(x.stdout+x.stderr).decode(errors='replace')
x=subprocess.run([java,'-cp',str(build)+';'+cp,'OptionalVirtualRadioPatch',str(r/'ui-compat/native-ui/network-ota-retained-v3/radio-classes.dex'),str(build/'classes.dex')],capture_output=True,timeout=40);assert x.returncode==0,(x.stdout+x.stderr).decode(errors='replace');print(x.stdout.decode(),flush=True)
p=r/'donor-tree/system_ext/framework/oplus-telephony-common.jar';out=build/p.name
assert hashlib.sha256(p.read_bytes()).hexdigest()=='23ea03782b135e10e4cecd84a4ffde1bc149a0f290325d6a54a1a89c3ac59568'
with zipfile.ZipFile(p) as original,zipfile.ZipFile(out,'w') as z:
 for i in original.infolist():z.writestr(i,(build/'classes.dex').read_bytes() if i.filename=='classes.dex' else original.read(i.filename))
with zipfile.ZipFile(p) as a,zipfile.ZipFile(out) as b:
 assert a.namelist()==b.namelist() and b.testzip() is None
 assert all(a.read(n)==b.read(n) for n in a.namelist() if n!='classes.dex')
x=subprocess.run([java,'-cp',str(r/'ui-compat/native-ui/stack-v4/compare-classes')+';'+cp,'CompareApkDex',str(p),str(out)],check=True,capture_output=True,timeout=60)
(build/'radio-diff.txt').write_bytes(x.stdout+x.stderr);s=x.stdout.decode();assert all(t in s for t in ['REMOVED 0','ADDED 0','CHANGED 2']);print(s[-1800:],flush=True)
(w/'radio-build.json').write_text(json.dumps({'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'changed_methods':2,'added_removed_members':0,'non_dex_entries_identical':True,'retry_argument':{'before':'non-MTK=true','after':False},'native_catch_and_fallback_unchanged':True,'no_fake_service_result':True,'runtime_verified':False},indent=2)+'\n')
