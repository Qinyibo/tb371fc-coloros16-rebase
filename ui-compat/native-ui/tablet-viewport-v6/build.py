from pathlib import Path
import hashlib,re,subprocess,sys,zipfile,json
root=Path.cwd();w=root/"ui-compat/native-ui/tablet-viewport-v6";build=w/"build"
sys.path.insert(0,str(root/"ui-compat/native-ui"))
from apk_container import append_dex,replace_dex
apk=root/"ui-compat/native-ui/stack-v4/build/launcher/OplusLauncher.apk"
original=apk.read_bytes()
assert hashlib.sha256(original).hexdigest()=="374c0ffb9b0ff9ef1b8f667a1219611ae6c01d3f973dde00c0527fdbb0a1fd1d"
libs=[p for p in Path("C:/android-sdk/cmdline-tools/latest/lib").rglob("*.jar") if any(k in str(p).lower() for k in ("smali","guava","failureaccess"))]
cp=";".join(map(str,libs));java="C:/Program Files/Java/jdk-21/bin/java.exe"
subprocess.run(["C:/Program Files/Java/jdk-21/bin/javac.exe","-cp",cp,"-d",str(build),str(w/"TabletViewportPatch.java")],check=True,timeout=30)
raw=original;changes=0
with zipfile.ZipFile(apk) as z:
 names=[n for n in z.namelist() if re.fullmatch(r"classes\d*\.dex",n)]
 for name in names:
  src=build/name;src.write_bytes(z.read(name));out=build/(name+".patched")
  run=subprocess.run([java,"-cp",str(build)+";"+cp,"TabletViewportPatch",str(src),str(out)],check=True,capture_output=True,timeout=60)
  log=run.stdout.decode();n=int(re.search(r"CHANGES (\d+)",log)[1]);changes+=n
  if n: raw=replace_dex(raw,name,out.read_bytes()); print(name,log.strip(),flush=True)
 assert changes==1,changes
 last=max(1 if n=="classes.dex" else int(re.search(r"\d+",n)[0]) for n in names)+1
 raw=append_dex(raw,f"classes{last}.dex",(build/"dex/classes.dex").read_bytes())
 target=build/"OplusLauncher.apk";target.write_bytes(raw)
 with zipfile.ZipFile(target) as out:
  assert out.testzip() is None
  assert all(out.read(n)==z.read(n) for n in z.namelist() if not re.fullmatch(r"classes\d*\.dex",n))
diff=subprocess.run([java,"-cp",cp,str(root/"ui-compat/native-ui/stack-v4/compare-classes")+";"+cp,"CompareApkDex",str(apk),str(target)],capture_output=True,timeout=90)
# The existing compiled comparator omits debug metadata and checks all members.
if diff.returncode:
 diff=subprocess.run([java,"-cp",cp,str(root/"camera-compat-native/tb-camera-unit/build/CompareApkDex.java"),str(apk),str(target)],check=True,capture_output=True,timeout=90)
(build/"diff.txt").write_bytes(diff.stdout+diff.stderr)
print(diff.stdout.decode()[-2400:],flush=True)
(w/"build.json").write_text(json.dumps({"source_sha256":hashlib.sha256(original).hexdigest(),"apk_sha256":hashlib.sha256(raw).hexdigest(),"changed_methods":changes,"non_dex_entries_identical":True,"runtime_verified":False,"oem_cryptographic_signature_valid":False},indent=2)+"\n")
