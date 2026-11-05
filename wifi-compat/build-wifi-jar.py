from pathlib import Path
import subprocess,zipfile,copy,hashlib,json
r=Path.cwd();w=r/'wifi-compat';a=w/'apex';src=a/'service-wifi.original.jar';assert hashlib.sha256(src.read_bytes()).hexdigest()=='1cf13331adcd54420cbe1d4e12db58cde2de3902c2dc840c9bf94584b04f64c5'
jdk=Path('C:/Program Files/Java/jdk-21/bin');libs=[p for p in Path('C:/android-sdk/cmdline-tools/latest/lib').rglob('*.jar') if any(k in str(p).lower() for k in ('smali','guava','failureaccess'))];cp=';'.join(map(str,libs))
subprocess.run([str(jdk/'javac.exe'),'-cp',cp,'-d',str(w),str(w/'WifiOptionalRadioStatsPatch.java'),str(r/'CompareDex.java')],check=True)
with zipfile.ZipFile(src) as z:(w/'wifi.original.dex').write_bytes(z.read('classes.dex'))
subprocess.run([str(jdk/'java.exe'),'-cp',str(w)+';'+cp,'WifiOptionalRadioStatsPatch',str(w/'wifi.original.dex'),str(w/'wifi.compat.dex')],check=True)
p=subprocess.run([str(jdk/'java.exe'),'-cp',str(w)+';'+cp,'CompareDex',str(w/'wifi.original.dex'),str(w/'wifi.compat.dex'),str(w/'canonical-diff'),'Lcom/android/server/wifi/WifiChannelUtilization;->public refreshChannelStatsAndChannelUtilization(Lcom/android/server/wifi/WifiLinkLayerStats;I)V'],capture_output=True,timeout=90);(w/'wifi-canonical-comparison.txt').write_bytes(p.stdout+p.stderr);assert p.returncode==0,(p.stdout+p.stderr).decode(errors='replace');print(p.stdout.decode(errors='replace'))
target=a/'service-wifi.compat.jar'
with zipfile.ZipFile(src) as z,zipfile.ZipFile(target,'w') as dst:
 for i in z.infolist():dst.writestr(copy.copy(i),(w/'wifi.compat.dex').read_bytes() if i.filename=='classes.dex' else z.read(i))
with zipfile.ZipFile(src) as z,zipfile.ZipFile(target) as dst:
 assert z.namelist()==dst.namelist() and dst.testzip() is None and all(z.read(n)==dst.read(n) for n in z.namelist() if n!='classes.dex')
(w/'jar-result.json').write_text(json.dumps({'before':hashlib.sha256(src.read_bytes()).hexdigest(),'after':hashlib.sha256(target.read_bytes()).hexdigest(),'scope':'One optional per-radio statistics array guard; no success synthesis; preserves original aggregate channel statistics path and full supported per-radio behavior','device_tested':False},indent=2)+'\n')
print('WIFI_SERVICE_JAR_BUILT')
