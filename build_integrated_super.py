import hashlib,importlib.util,json,pathlib,struct,subprocess,sys
r=pathlib.Path(sys.argv[1]); dest=r/('integrated-network' if '--network' in sys.argv[2:] else 'integrated-logicals')
repo=pathlib.Path('/mnt/d/TB371FC-release/public-source/TB371FC-ColorOS16')
tool=pathlib.Path('/mnt/d/vivo/新建文件夹/中轴门/TB371FC_ColorOS16/tools/aosp-build-tools/android16/linux-x86/bin/lpmake')
old=pathlib.Path('/mnt/d/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/images/super-R94.img')
spec=importlib.util.spec_from_file_location('lp',repo/'rom-build/tools/lp_probe.py');lp=importlib.util.module_from_spec(spec);spec.loader.exec_module(lp)
def metadata(p):
 with p.open('rb') as f: head=f.read(2<<20)
 g=lp.parse_geometry(head); m=lp.parse_metadata(head,g)
 o=m['header']['metadata_region_offset']; assert head[o:o+4]==b'0PLA'
 t=o+m['header']['header_size']
 def rows(i,fmt):
  a,n,w=struct.unpack_from('<III',head,o+80+i*12)
  assert struct.calcsize(fmt)==w
  return [struct.unpack_from(fmt,head,t+a+j*w) for j in range(n)]
 groups=[(name.split(b'\0')[0].decode(),flags,max_) for name,flags,max_ in rows(2,'<36sIQ')]
 devices=[(name.split(b'\0')[0].decode(),first,alignment,offset,size,flags) for first,alignment,offset,size,name,flags in rows(3,'<QIIQ36sI')]
 flags,=struct.unpack_from('<I',head,o+128)
 return g,m,groups,devices,flags
g,m,groups,devices,flags=metadata(old)
name,first,alignment,offset,size,dflags=devices[0]
assert len(devices)==1 and (name,dflags,flags)==('super',0,1)
limits={name:max_ for name,group_flags,max_ in groups}
meta_size,slots,bs=g['metadata_max_size'],g['metadata_slot_count'],g['logical_block_size']
target=dest/('super-cleanbase-network-OFFLINE.img' if '--network' in sys.argv[2:] else 'super-cleanbase-OFFLINE.img')
verify_existing="--verify-existing" in sys.argv[2:]
assert target.exists()==verify_existing
images={f'{n}_a':dest/(n+'.img') for n in ['system','system_ext','product']}
images.update({f'{n}_a':r/'tb-inputs'/(n+'_a.img') for n in ['vendor','odm']})
args=[tool,'--device',f'{name}:{size}:{alignment}:{offset}','--metadata-size',str(meta_size),'--metadata-slots',str(slots),'--block-size',str(bs),'--virtual-ab','--output',target]
for name,group_flags,max_ in groups:
 assert group_flags==0
 if name!='default':args+=['--group',f'{name}:{max_}']
sizes={}
for p in m['partitions']:
 n=p['name']; group=p['group']; a=p['attributes']
 assert a in (0,1) and (n in images or n.endswith('_b'))
 b=images[n].stat().st_size if n in images else 0
 sizes[n]=b
 args+=['--partition',f'{n}:{"readonly" if a else "none"}:{b}:{group}']
 if n in images:args+=['--image',f'{n}={images[n]}']
for name,limit in limits.items():
 if not limit:continue
 assert sum(sizes[p['name']] for p in m['partitions'] if p['group']==name)<=limit
if not verify_existing:
 with (dest/'lpmake.log').open('wb') as log:
  subprocess.run(args,stdout=log,stderr=subprocess.STDOUT,check=True)
gn,mn,new_groups,new_devices,new_flags=metadata(target)
assert (gn,new_groups,new_flags)==(g,groups,flags)
nd=new_devices[0]
assert len(new_devices)==1 and nd[:1]+nd[2:]==devices[0][:1]+devices[0][2:]
assert target.stat().st_size==old.stat().st_size
metadata_end=4096*3+2*meta_size*slots
assert metadata_end<=nd[1]*512 and nd[1]*512%alignment==0
with target.open('rb') as f:
 f.seek(4096); a=f.read(4096); b=f.read(4096)
 assert a==b
 gz=bytearray(a[:g['struct_size']]);digest=gz[8:40];gz[8:40]=b'\0'*32
 assert hashlib.sha256(gz).digest()==digest
 for i in range(slots):
  f.seek(12288+i*meta_size); a=f.read(meta_size)
  f.seek(12288+(slots+i)*meta_size); b=f.read(meta_size)
  assert a==b and a[:4]==b'0PLA'
  hsize=struct.unpack_from('<I',a,8)[0]; tsize=struct.unpack_from('<I',a,44)[0]
  header=bytearray(a[:hsize]); digest=header[12:44];header[12:44]=b'\0'*32
  assert hashlib.sha256(header).digest()==digest
  assert hashlib.sha256(a[hsize:hsize+tsize]).digest()==a[48:80]
assert {(p['name'],p['group'],p['attributes'],sizes[p['name']]) for p in m['partitions']}=={(p['name'],p['group'],p['attributes'],p['size_bytes']) for p in mn['partitions']}
digests={n:hashlib.sha256() for n in images}; extents=[]
for p in mn['partitions']:
 n=p['name']
 if n not in images:
  assert not p['extents'];continue
 assert len(p['extents'])==1 and p['size_bytes']==sizes[n]
 for e in p['extents']:
  assert e['type']==e['source']==0
  start=e['target_data']*512
  assert start%alignment==0 and start>=nd[1]*512 and start+p['size_bytes']<=size
  extents.append((start,p['size_bytes'],n))
recorded={pathlib.Path(p).stem:h for h,p in (line.split() for line in (dest/'SHA256SUMS').read_text().splitlines())}
recorded.update({k:v['sha256'] for k,v in json.loads((r/'tb-inputs/source.json').read_text())['partitions'].items()})
full=hashlib.sha256(); result={}
with target.open('rb') as f:
 def consume(left,own=None):
  while left:
   chunk=f.read(min(left,16<<20));assert chunk
   full.update(chunk)
   if own:own.update(chunk)
   left-=len(chunk)
 for start,count,n in sorted(extents):
  assert f.tell()<=start
  consume(start-f.tell())
  consume(count,digests[n])
  expect=recorded[n if n in recorded else n[:-2]]
  actual=digests[n].hexdigest()
  assert actual==expect,(n,actual,expect)
  result[n]=dict(bytes=count,sha256=actual,start_sector=start//512)
  print('SUPER_LOGICAL_HASH_PASS',n,flush=True)
 consume(size-f.tell())
digest=full.hexdigest()
(dest/'super-result.json').write_text(json.dumps(dict(scope='Offline only; all LP metadata CRCs, layout and full extent content verified',sha256=digest,bytes=target.stat().st_size,first_logical_sector_before=first,first_logical_sector_candidate=nd[1],metadata_end_sector=metadata_end//512,logical_partitions=result),indent=2)+'\n')
print('SUPER_FULL_EXTENT_HASH_PASS',digest,flush=True)
