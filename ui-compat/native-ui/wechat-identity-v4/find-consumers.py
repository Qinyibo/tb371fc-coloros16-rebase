from pathlib import Path
import subprocess
r=Path.cwd(); w=r/'ui-compat/native-ui/wechat-identity-v4'
cp=';'.join(str(p) for p in Path('C:/android-sdk/cmdline-tools/latest/lib').rglob('*.jar') if any(t in str(p).lower() for t in ['smali','guava','failureaccess']))
java='C:/Program Files/Java/jdk-21/bin/'
subprocess.run([java+'javac.exe','-cp',cp,'-d',str(w),str(w/'FindIdentityConsumers.java')],check=True,timeout=30)
x=subprocess.run([java+'java.exe','-Xmx2g','-cp',str(w)+';'+cp,'FindIdentityConsumers',str(w/'installed-original.apk')],capture_output=True,timeout=90)
(w/'native-identity-consumers.txt').write_bytes(x.stdout+x.stderr)
assert x.returncode==0, x.stderr
print(x.stdout.decode())
