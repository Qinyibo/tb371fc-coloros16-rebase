import json,os,pathlib,stat,sys
r=pathlib.Path(sys.argv[1]);result={}
for name in ['system','system_ext']:
 sources=[('',r/'mounts'/name)]
 if name=='system':sources += [(n,r/'mounts'/n) for n in ['my_product','my_stock','my_manifest','my_region','my_engineering','my_carrier','my_heytap','my_bigball']]
 commands=[]
 for prefix,root in sources:
  for parent,dirs,files in os.walk(root,followlinks=False):
   for n in dirs+files:
    p=pathlib.Path(parent)/n;s=p.lstat()
    if not stat.S_ISLNK(s.st_mode):continue
    rel=pathlib.Path(prefix)/p.relative_to(root);target=r/'mounts'/('build-'+name)/rel
    t=target.lstat();assert stat.S_ISLNK(t.st_mode) and os.readlink(p)==os.readlink(target)
    if s.st_mode!=t.st_mode:commands.append(f'set_inode_field {json.dumps("/"+str(rel))} mode 0{s.st_mode:o}')
 (r/'base-ext4-UNADAPTED'/(name+'-symlink-modes.debugfs')).write_text('\n'.join(commands)+'\n')
 result[name]=len(commands)
(r/'base-ext4-UNADAPTED/symlink-mode-corrections.json').write_text(json.dumps(result,indent=2))
print(result)
