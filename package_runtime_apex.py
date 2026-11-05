import copy,hashlib,json,pathlib,subprocess,zipfile
r=pathlib.Path(__file__).resolve().parent;out=r/'apex-ext4-prototype/com.android.runtime';keys=r/'private-signing/apex/com.android.runtime'
source=r/'donor-tree/system/system/apex/com.android.runtime.apex'
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
expected=next(x for x in json.loads((r/'apex-inputs/source.json').read_text()) if x['name']=='com.android.runtime')['sha256'];assert sha(source)==expected
unsigned=out/'unsigned.zip';aligned=out/'aligned.apex';signed=out/'com.android.runtime.ext4.apex';assert not signed.exists()
changed={'apex_payload.img','apex_pubkey'}
def signature_member(n):return n.startswith('META-INF/') and (n.upper().endswith(('.RSA','.DSA','.EC','.SF')) or n.upper()=='META-INF/MANIFEST.MF')
with zipfile.ZipFile(source) as z,zipfile.ZipFile(unsigned,'w') as dest:
 for i in z.infolist():
  if signature_member(i.filename):continue
  entry=copy.copy(i)
  if i.filename in changed:entry.compress_type=zipfile.ZIP_STORED
  dest.writestr(entry,(out/i.filename).read_bytes() if i.filename in changed else z.read(i))
sdk=pathlib.Path('C:/android-sdk/build-tools/36.0.0');java='C:/Program Files/Java/jdk-21/bin/java.exe'
subprocess.run([str(sdk/'zipalign.exe'),'-f','4096',str(unsigned),str(aligned)],check=True)
signer=[java,'-jar',str(sdk/'lib/apksigner.jar')]
p=subprocess.run([*signer,'sign','--key',str(keys/'container.pk8'),'--cert',str(keys/'container.x509.pem'),'--min-sdk-version','29','--v1-signing-enabled','false','--v2-signing-enabled','true','--v3-signing-enabled','true','--v4-signing-enabled','false','--out',str(signed),str(aligned)],capture_output=True,text=True);(out/'container-sign.log').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr
p=subprocess.run([*signer,'verify','--verbose','--print-certs',str(signed)],capture_output=True,text=True);(out/'container-verification.log').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr
assert 'Verified using v3 scheme (APK Signature Scheme v3): true' in p.stdout,p.stdout
subprocess.run([str(sdk/'zipalign.exe'),'-c','4096',str(signed)],check=True)
with zipfile.ZipFile(source) as before,zipfile.ZipFile(signed) as after:
 assert after.testzip() is None
 assert set(after.namelist())=={n for n in before.namelist() if not signature_member(n)}
 assert all(before.read(n)==after.read(n) for n in after.namelist() if n not in changed)
 assert all(after.read(n)==(out/n).read_bytes() for n in changed)
 i=after.getinfo('apex_payload.img')
 with signed.open('rb') as f:
  f.seek(i.header_offset);h=f.read(30)
 import struct
 payload_offset=i.header_offset+30+sum(struct.unpack_from('<HH',h,26));assert payload_offset%4096==0
result=dict(state='OFFLINE_PROTOTYPE_ONLY_NOT_ADOPTED_OR_INSTALLED',source_version='OPD2413_16.0.10.600(CN01)',source_apex_sha256=expected,output_apex_sha256=sha(signed),bytes=signed.stat().st_size,source_code_and_config_files_changed=False,payload_filesystem='ext4',source_tree_contents_and_metadata_equal=json.loads((out/'content-verification.json').read_text())['all_equal'],payload_avb_signed_and_hashtree_verified=True,container_v3_signature_verified=True,payload_zip_offset=payload_offset,signature_keys='Unique project prototype payload/container keys retained privately on D; original OEM signature intentionally replaced, not claimed preserved',unchanged_zip_members_verified=True,device_tested=False,adoption_requires=['Boot/APEX manager compatibility evidence','Package-specific durable signing/upgrade ownership','Full-super capacity budget and reproducible all-package build','No loss of required native system components'])
(out/'build-result.json').write_text(json.dumps(result,indent=2));print('RUNTIME_APEX_EXT4_DUAL_SIGNATURE_OFFLINE_PASS',signed.stat().st_size)
