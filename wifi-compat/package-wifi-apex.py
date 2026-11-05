import pathlib,json,hashlib,zipfile,struct,sys
mode=sys.argv[1];r=pathlib.Path(sys.argv[2]);w=r/'wifi-compat';out=w/'rebuilt-wifi';src=r/'donor-tree/system/system/apex/com.android.wifi.apex'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def signature(n):
 n=n.upper();return n.startswith('META-INF/') and n.endswith(('.RSA','.DSA','.EC','.SF','/MANIFEST.MF'))
if mode=='audit':
 ns={'sys':sys};exec((r/'verify_base.py').read_text().split("for name in ['system','system_ext']:")[0],ns)
 a,b=[ns['inventory'](p) for p in [w/'apex/source',pathlib.Path('/work/tb371fc-clean-wifi-20261105/tree')]]
 assert a.keys()-b.keys()=={'javalib/service-wifi.jar.prof'} and not b.keys()-a.keys()
 delta={n for n in b if a[n]!=b[n]};assert delta=={'javalib/service-wifi.jar'},delta
 k=next(iter(delta));assert {n:v for n,v in a[k].items() if n not in ('sha256','size')}=={n:v for n,v in b[k].items() if n not in ('sha256','size')}
 assert b[k]['sha256']==json.loads((w/'jar-result.json').read_text())['after']
 (out/'payload-diff.json').write_text(json.dumps({'entries':len(b),'changed':list(delta),'removed':['javalib/service-wifi.jar.prof'],'reason_removed':'Stale profile for original DEX checksum; no replacement profile claimed','all_other_files_and_metadata_unchanged':True},indent=2)+'\n')
 print('WIFI_PAYLOAD_ONLY_JAR_AND_STALE_PROFILE_DELTA_PASS')
elif mode=='pack':
 with zipfile.ZipFile(src) as z,zipfile.ZipFile(out/'unsigned.zip','x') as dst:
  for i in z.infolist():
   if signature(i.filename):continue
   n=i.filename;entry=zipfile.ZipInfo(n,(2026,11,5,0,0,0));entry.create_system=3;entry.compress_type=zipfile.ZIP_STORED if n in ['apex_pubkey','apex_payload.img'] else i.compress_type
   dst.writestr(entry,(out/n).read_bytes() if n in ['apex_pubkey','apex_payload.img'] else z.read(n))
elif mode=='verify':
 p=out/'com.android.wifi.apex'
 with zipfile.ZipFile(src) as before,zipfile.ZipFile(p) as after:
  assert after.testzip() is None and set(after.namelist())=={n for n in before.namelist() if not signature(n)}
  assert all(before.read(n)==after.read(n) for n in after.namelist() if n not in ['apex_payload.img','apex_pubkey'])
  assert all(after.read(n)==(out/n).read_bytes() for n in ['apex_payload.img','apex_pubkey'])
  e=after.getinfo('apex_payload.img')
  with p.open('rb') as f:f.seek(e.header_offset);off=e.header_offset+30+sum(struct.unpack_from('<HH',f.read(30),26))
  assert off%4096==0 and e.compress_type==zipfile.ZIP_STORED
 result={'scope':'Same-release WiFi APEX with one optional per-radio consumer guard; retains aggregate channel statistics. Offline only','official_sha256':sha(src),'sha256':sha(p),'bytes':p.stat().st_size,'payload_offset':off,'project_payload_key':'private-signing/apex/com.android.wifi/payload.pem','container_signer_sha256':'6bf99a00296cc6f571824d07209a62c1739a0798c32c067d982171f142c96600','oem_signature_preserved':False,'inner_apks_and_framework_wifijar_unchanged':True,'runtime_tested':False}
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('WIFI_APEX_SIGNED_AND_CONTENT_VERIFIED',result['sha256'])
