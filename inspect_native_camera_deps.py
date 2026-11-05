import json,os,pathlib,re,subprocess,sys,zipfile
r=pathlib.Path(sys.argv[1]); m=r/'mounts'
out=r/'camera-compat-native';out.mkdir(exist_ok=False)
apk=m/'my_product/app/OplusCamera/OplusCamera.apk'
folders={p.relative_to(m).as_posix():p for p in [m/'system/system/lib64',m/'system_ext/lib64',m/'product/lib64',m/'my_product/lib64',m/'my_stock/lib64',m/'tb-vendor/lib64',m/'tb-odm/lib64',m/'com.android.vndk.v30/lib64',m/'com.android.runtime/lib64/bionic']}
idx={}
for label,root in folders.items():
 if not root.is_dir():continue
 for p in root.iterdir():
  if p.name.endswith('.so'):idx.setdefault(p.name,[]).append(label)
result={}
with zipfile.ZipFile(apk) as z:
 libs={p.rsplit('/',1)[-1]:p for p in z.namelist() if re.fullmatch(r'lib/arm64-v8a/[^/]+\.so',p)}
 for n,p in libs.items():
  t=out/n;t.write_bytes(z.read(p))
  s=subprocess.check_output(['aarch64-linux-gnu-readelf','-d',t],text=True)
  req=re.findall(r'\(NEEDED\).*\[([^\]]+)\]',s)
  result[n]={k:['apk']+idx.get(k,[]) if k in libs else idx.get(k,[]) for k in req}
  t.unlink()
missing={n:[k for k,v in req.items() if not v] for n,req in result.items() if any(not v for v in req.values())}
(out/'result.json').write_text(json.dumps(dict(scope='APK direct DT_NEEDED in named roots; no namespace, dlopen, HAL or physical camera proof',native_libraries=len(result),apk=str(apk),missing_in_checked_roots=missing,dependency_locations=result),indent=2)+'\n')
print('COLOROS_CAMERA_STATIC_DEPS',len(result),json.dumps(missing))
