from pathlib import Path
import subprocess,json,hashlib
o=Path(__file__).resolve().parent;build=o/'build';build.mkdir(exist_ok=True)
libs=[p for p in Path('C:/android-sdk/cmdline-tools/latest/lib').rglob('*.jar') if any(x in str(p).lower() for x in ['smali','guava','failureaccess'])];cp=';'.join(map(str,libs));j=Path('C:/Program Files/Java/jdk-21/bin')
p=subprocess.run([str(j/'javac.exe'),'-cp',cp,'-d',str(build),str(o/'PenContracts.java')],capture_output=True);(build/'compile.log').write_bytes(p.stdout+p.stderr);assert p.returncode==0,p.stderr.decode(errors='replace')
for name in ['IPeManager-current.apk','WirelessSettings-current.apk']:
 p=subprocess.run([str(j/'java.exe'),'-cp',str(build)+';'+cp,'PenContracts',str(o/name)],capture_output=True,timeout=50);(o/(name+'.contracts-v2.txt')).write_bytes(p.stdout+p.stderr);assert p.returncode==0
 print(name,'contract bytes',len(p.stdout),'sha256',hashlib.sha256((o/name).read_bytes()).hexdigest())
(o/'dex-classpath.json').write_text(json.dumps({'cp':cp,'java':str(j)},indent=2))
