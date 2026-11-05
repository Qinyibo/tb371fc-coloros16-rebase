import gzip,hashlib,json,os,pathlib,shutil,stat,subprocess,sys,zipfile
r=pathlib.Path(sys.argv[1]); out=r/'erofs-lz4-ab/corpus'
out.mkdir(exist_ok=False)
mnt=out/'mount';mnt.mkdir(); results=[]
sets=[]; batch=[]; size=0
for x in json.loads((r/'apex-filesystem-inventory.json').read_text()):
 if x['filesystem']!='erofs': continue
 if batch and (len(batch)==4 or size+x['payload_bytes']>48<<20):
  sets.append(batch);batch=[];size=0
 batch.append(x);size+=x['payload_bytes']
if batch:sets.append(batch)
for j,batch in enumerate(sets):
 dest=out/f'batch-{j:02d}.cpio.gz'
 with dest.open('wb') as raw,gzip.GzipFile(fileobj=raw,mode='wb',mtime=0,compresslevel=2) as archive:
  ino=1; pos=0
  def add(name,mode,data=b'',uid=0,gid=0,major=0,minor=0):
   global ino,pos
   n=name.encode()+b'\0';v=[ino,mode,uid,gid,1,0,len(data),0,0,major,minor,len(n),0];ino+=1
   p=b'070701'+''.join(f'{x:08x}' for x in v).encode()+n
   archive.write(p);pos+=len(p); pad=-pos%4;archive.write(b'\0'*pad);pos+=pad
   archive.write(data);pos+=len(data);pad=-pos%4;archive.write(b'\0'*pad);pos+=pad
  for d in ('dev','proc','sys','erofs','reference','payload'):add(d,0o40755)
  add('dev/console',0o20600,major=5,minor=1);add('dev/null',0o20666,major=1,minor=3)
  add('init',0o100755,(r/'erofs-lz4-ab/corpus-init').read_bytes())
  add('trial.ko',0o100644,(r/'erofs-lz4-ab/vm-partial/erofs.ko').read_bytes())
  add('packages',0o100644,('\n'.join(x['package'] for x in batch)+'\n').encode())
  for i,item in enumerate(batch):
   p=out/'current-original.img'
   with zipfile.ZipFile(r/'mounts'/item['package']) as z:
    with z.open('apex_payload.img') as src,p.open('xb') as dst: shutil.copyfileobj(src,dst,8<<20)
   data=p.read_bytes()
   assert len(data)==item['payload_bytes']
   add(f'payload/{i}',0o100444,data)
   row=dict(package=item['package'],batch=j,index=i,sha256=hashlib.sha256(data).hexdigest(),files=0,dirs=0,links=0,bytes=0)
   del data
   subprocess.run(['mount','-t','erofs','-o','ro,loop',p,mnt],check=True)
   def copy(f,name):
    s=f.lstat()
    if stat.S_ISREG(s.st_mode):
     data=f.read_bytes();row['files']+=1;row['bytes']+=len(data)
    elif stat.S_ISDIR(s.st_mode):
     data=b'';row['dirs']+=1
    elif stat.S_ISLNK(s.st_mode):
     data=os.readlink(f).encode();row['links']+=1
    else:raise ValueError((f,s.st_mode))
    add(name,s.st_mode,data,s.st_uid,s.st_gid)
   try:
    ref=f'reference/{i}'
    copy(mnt,ref)
    for parent,dirs,files in os.walk(mnt,followlinks=False):
     for n in sorted(dirs+files):
      f=pathlib.Path(parent)/n; copy(f,ref+'/'+str(f.relative_to(mnt)))
   finally: subprocess.run(['umount',mnt],check=True)
   p.unlink()
   results.append(row)
  add('TRAILER!!!',0)
 print(f'BUILT {dest.name} {len(batch)} packages',flush=True)
(out/'manifest.json').write_text(json.dumps(results,indent=2)+'\n')
