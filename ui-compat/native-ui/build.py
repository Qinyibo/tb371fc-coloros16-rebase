from pathlib import Path
import subprocess,zipfile,re,hashlib,json,struct,argparse
from apk_container import replace_dex,append_dex

parser=argparse.ArgumentParser();parser.add_argument('--only',action='append',choices=['launcher','settings','assistant']);parser.add_argument('--output',default='build');args=parser.parse_args()
w=Path(__file__).resolve().parent;r=w.parent.parent;j=Path('C:/Program Files/Java/jdk-21/bin');sdk=Path('C:/android-sdk');bt=sdk/'build-tools/36.0.0';android=sdk/'platforms/android-36/android.jar';out=(w/args.output).resolve();assert out.is_relative_to(w);out.mkdir(parents=True,exist_ok=True)
def run(args,name):
    p=subprocess.run(list(map(str,args)),capture_output=True,timeout=150)
    (out/(name+'.log')).write_bytes(p.stdout+p.stderr)
    if p.returncode:raise RuntimeError(name+'\n'+(p.stdout+p.stderr).decode(errors='replace')[-3000:])
    return p.stdout.decode(errors='replace')
libs=[p for p in (sdk/'cmdline-tools/latest/lib').rglob('*.jar') if any(k in str(p).lower() for k in ('smali','guava','failureaccess'))];cp=';'.join(map(str,libs));patcher=out/'patcher';patcher.mkdir(exist_ok=True)
run([j/'javac.exe','-cp',cp,'-d',patcher,w/'AnimationDexPatch.java'],'compile-patcher')
stubs=out/'stubs';stubs.mkdir(exist_ok=True)
run([j/'javac.exe','--release','8','-cp',android,'-d',stubs,*list((w/'stubs').rglob('*.java'))],'compile-stubs')
stubjar=out/'stubs.jar'
with zipfile.ZipFile(stubjar,'w') as z:
    for p in stubs.rglob('*.class'):z.write(p,p.relative_to(stubs).as_posix())
helpers={}
for mode,source in [('launcher','LauncherCompat.java'),('settings','AnimationSettings.java')]:
    if args.only and mode not in args.only:continue
    c=out/(mode+'-helper-classes');c.mkdir(exist_ok=True)
    run([j/'javac.exe','--release','8','-cp',str(android)+';'+str(stubjar),'-d',c,w/'src/org/tb371fc/animation'/source],mode+'-helper-javac')
    jar=out/(mode+'-helper.jar')
    with zipfile.ZipFile(jar,'w') as z:
        for p in c.rglob('*.class'):z.write(p,p.relative_to(c).as_posix())
    d=out/(mode+'-helper-dex');d.mkdir(exist_ok=True)
    run([j/'java.exe','-cp',bt/'lib/d8.jar','com.android.tools.r8.D8','--min-api','35','--lib',android,'--classpath',stubjar,'--output',d,jar],mode+'-helper-d8')
    helpers[mode]=(d/'classes.dex').read_bytes()
sources={'launcher':r/'donor-tree/system_ext/priv-app/OplusLauncher/OplusLauncher.apk','settings':r/'donor-tree/system_ext/priv-app/Settings/Settings.apk','assistant':r/'donor-tree-case/my_stock/app/AssistantScreen/AssistantScreen.apk'}
rows={}
def signing_block(raw):
    eocd=raw.rfind(b'PK\x05\x06');off=struct.unpack_from('<I',raw,eocd+16)[0];assert raw[off-16:off]==b'APK Sig Block 42';size=struct.unpack_from('<Q',raw,off-24)[0]+8
    return raw[off-size:off]
for mode,src in sources.items():
    if args.only and mode not in args.only:continue
    raw=src.read_bytes();original=raw;stage=out/mode;stage.mkdir(exist_ok=True);moved=[];edits=[];changed=[]
    if mode=='launcher':assert hashlib.sha256(raw).hexdigest()=='938ba50c04badeb3483316c9539200891a126d8d1a3f618d01e14bbfb47ab907'
    with zipfile.ZipFile(src) as z:
        names=[n for n in z.namelist() if re.fullmatch(r'classes\d*\.dex',n)]
        for name in names:
            inp=stage/name;inp.write_bytes(z.read(name));patched=stage/(name+'.patched')
            log=run([j/'java.exe','-cp',str(patcher)+';'+cp,'AnimationDexPatch',inp,patched,mode],mode+'-'+name)
            count=int(re.search(r'PATCHED (\d+)',log)[1])
            if count:
                edits.extend(log.strip().splitlines());raw=replace_dex(raw,name,patched.read_bytes());changed.append(name)
                if mode!='assistant':moved.append(Path(str(patched)+'.moved').read_bytes())
        assert edits,mode
        if mode in helpers:moved.append(helpers[mode])
        last=max(1 if n=='classes.dex' else int(re.search(r'\d+',n)[0]) for n in names)
        for b in moved:
            last+=1;name=f'classes{last}.dex';raw=append_dex(raw,name,b);changed.append(name)
        dest=stage/src.name;dest.write_bytes(raw)
        assert signing_block(original)==signing_block(raw)
        with zipfile.ZipFile(dest) as dz:
            assert dz.testzip() is None and set(z.namelist())<=set(dz.namelist())
            assert all(z.read(n)==dz.read(n) for n in z.namelist() if not re.fullmatch(r'classes\d*\.dex',n))
            for n in z.namelist():
                if n.startswith('lib/') and n.endswith('.so') and z.getinfo(n).compress_type==0:
                    def offset(archive,data):
                        h=archive.getinfo(n).header_offset;nl,el=struct.unpack_from('<HH',data,h+26);return h+30+nl+el
                    assert offset(z,original)%4096==offset(dz,raw)%4096==0,n
    rows[mode]={'input':str(src.relative_to(r)),'input_sha256':hashlib.sha256(original).hexdigest(),'output':str(dest.relative_to(r)),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'changed_dex':changed,'edits':edits,'non_dex_contents_preserved':True,'native_library_4k_alignment_preserved':True,'original_signing_identity_block_preserved':True,'original_oem_cryptographic_signature_valid':False,'signing_scope':'Modified trusted-preload APK for this unlocked image. Retains original identity for existing signature-only system interfaces; no signature-verification bypass patch added. Must not be represented as an OEM-signed APK or installed as an ordinary signed update.','physical_verified':False}
    print(mode,*edits,sep='\n',flush=True)
(out/'result.json').write_text(json.dumps(rows,indent=2)+'\n')
print('NEW_NATIVE_UI_APKS_BUILT_PENDING_CANONICAL_AND_PHYSICAL_VALIDATION',flush=True)
