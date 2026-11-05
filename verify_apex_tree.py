import hashlib,json,os,pathlib,stat,sys
source,dest,out=map(pathlib.Path,sys.argv[1:4]);mode=sys.argv[4]
def inventory(root):
 result={}
 def entry(p):
  s=p.lstat();v=dict(mode=s.st_mode,uid=s.st_uid,gid=s.st_gid,xattrs={n:os.getxattr(p,n,follow_symlinks=False).hex() for n in os.listxattr(p,follow_symlinks=False)})
  if stat.S_ISREG(s.st_mode):
   with p.open('rb') as f:v['sha256']=hashlib.file_digest(f,'sha256').hexdigest()
   v['bytes']=s.st_size
  elif stat.S_ISLNK(s.st_mode):v['link']=os.readlink(p)
  return v
 result['.']=entry(root)
 for parent,dirs,files in os.walk(root,followlinks=False):
  for n in dirs+files:
   p=pathlib.Path(parent)/n;result[str(p.relative_to(root))]=entry(p)
 return result
a,b=inventory(source),inventory(dest);assert set(a)==set(b),(set(a)^set(b));commands=[]
for n in a:
 if a[n]==b[n]:continue
 aa,bb=dict(a[n]),dict(b[n])
 assert mode=='prepare' and stat.S_ISLNK(aa['mode']) and aa.pop('mode')!=bb.pop('mode') and aa==bb,(n,a[n],b[n])
 commands.append(f'set_inode_field {json.dumps("/"+n)} mode 0{a[n]["mode"]:o}')
if mode=='prepare':(out/'symlink-modes.debugfs').write_text('\n'.join(commands)+'\n')
else:
 (out/'content-verification.json').write_text(json.dumps(dict(scope='Filesystem conversion only; original same-release APEX file contents, permissions, owners, symlinks and xattrs preserved',entries=len(a),regular_files=sum('sha256' in v for v in a.values()),all_equal=True),indent=2))
print('APEX_TREE_'+mode.upper()+'_PASS',len(a))
