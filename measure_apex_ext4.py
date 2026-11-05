import json,os,pathlib,shutil,stat,subprocess,zipfile
r=pathlib.Path('/mnt/d/TB371FC-release/clean-rebase-20261104')
w=r/'apex-ext4-sizing'; w.mkdir(exist_ok=False)
mnt=w/'mount'; mnt.mkdir(); p=w/'payload.img'; results=[]
zero=bytes(4096)
for item in json.loads((r/'apex-filesystem-inventory.json').read_text()):
 if item['filesystem']!='erofs': continue
 source=r/'mounts'/item['package']
 with zipfile.ZipFile(source) as z,z.open('apex_payload.img') as src,p.open('wb') as dst: shutil.copyfileobj(src,dst,8<<20)
 subprocess.run(['mount','-t','erofs','-o','ro,loop',p,mnt],check=True)
 try:
  seen=set(); files=bytes_=blocks=nonzero_blocks=0
  for path,dirs,names in os.walk(mnt):
   for n in names:
    f=pathlib.Path(path)/n;s=f.lstat()
    if not stat.S_ISREG(s.st_mode) or s.st_ino in seen: continue
    seen.add(s.st_ino); files+=1;bytes_+=s.st_size;blocks+=(s.st_size+4095)//4096
    with f.open('rb') as fh:
     while b:=fh.read(4096): nonzero_blocks+=any(b) if len(b)<4096 else b!=zero
  results.append(dict(package=item['package'],payload_bytes=p.stat().st_size,regular_files=files,logical_bytes=bytes_,ext4_data_bytes=blocks*4096,ext4_sparse_lower_bound=nonzero_blocks*4096))
 finally: subprocess.run(['umount',mnt],check=True)
 p.unlink()
(w/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(len(results),{k:sum(a[k] for a in results) for k in ('payload_bytes','logical_bytes','ext4_data_bytes','ext4_sparse_lower_bound')})

