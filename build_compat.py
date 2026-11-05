import copy,hashlib,json,pathlib,shutil,subprocess,zipfile
r=pathlib.Path(__file__).resolve().parent;repo=pathlib.Path('D:/TB371FC-release/public-source/TB371FC-ColorOS16')
source=r/'donor-tree/system/system/framework/oplus-services.jar'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(source)=='6d1280e25d0c40c12d1ed31877cfff40696d8d88cc089db5128cc2747c0bc7f2'
out=r/'compat-framework';assert not out.exists();out.mkdir()
jdk=pathlib.Path('C:/Program Files/Java/jdk-21/bin')
libs=[p for p in pathlib.Path('C:/android-sdk/cmdline-tools/latest/lib').rglob('*.jar') if any(k in str(p).lower() for k in ('smali','guava','failureaccess'))]
cp=';'.join(map(str,libs));sources=[]
for sub,name in [('native-charger','ChargerCompatPatch'),('native-freezer','FreezerFallbackPatch')]:
 p=out/(name+'.java');shutil.copyfile(repo/sub/(name+'.java'),p);sources.append(p)
subprocess.run([str(jdk/'javac.exe'),'-cp',cp,'-d',str(out),*map(str,sources)],check=True)
with zipfile.ZipFile(source) as z:(out/'original.dex').write_bytes(z.read('classes.dex'))
previous='original.dex'
for name,prefix in [('ChargerCompatPatch','charger'),('FreezerFallbackPatch','freezer')]:
 dest=prefix+'.dex'
 subprocess.run([str(jdk/'java.exe'),'-cp',str(out)+';'+cp,name,str(out/previous),str(out/dest),str(out/(prefix+'-focus.dex')),str(out/(prefix+'-before-focus.dex'))],check=True)
 previous=dest
target=out/'oplus-services.compat.jar'
with zipfile.ZipFile(source) as src,zipfile.ZipFile(target,'w') as dst:
 for i in src.infolist():dst.writestr(copy.copy(i),(out/previous).read_bytes() if i.filename=='classes.dex' else src.read(i))
with zipfile.ZipFile(source) as src,zipfile.ZipFile(target) as dst:
 assert dst.testzip() is None and src.namelist()==dst.namelist()
 assert all(src.read(n)==dst.read(n) for n in src.namelist() if n!='classes.dex')
(out/'build-result.json').write_text(json.dumps(dict(input_sha256=sha(source),output_sha256=sha(target),patch_sources={p.name:sha(p) for p in sources},scope='Offline DEX build only; not installed or integrated; stale stock fsv_meta/boot artifacts must not accompany changed JAR',device_tested=False),indent=2))
print('NEW_DONOR_COMPAT_JAR_BUILT',sha(target))
