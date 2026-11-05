import hashlib,json,os,pathlib,stat,sys
r=pathlib.Path(sys.argv[1]);results={}
def inventory(root):
    out={}
    def entry(p):
        s=p.lstat();d=dict(mode=s.st_mode,uid=s.st_uid,gid=s.st_gid,rdev=s.st_rdev)
        d['xattrs']={k:os.getxattr(p,k,follow_symlinks=False).hex() for k in os.listxattr(p,follow_symlinks=False)}
        if stat.S_ISLNK(s.st_mode):d['link']=os.readlink(p)
        if stat.S_ISREG(s.st_mode):
            d['size']=s.st_size
            with p.open('rb') as f:d['sha256']=hashlib.file_digest(f,'sha256').hexdigest()
        return d
    out['.']=entry(root)
    for parent,dirs,files in os.walk(root,followlinks=False):
        for n in dirs+files:
            p=pathlib.Path(parent)/n;out[str(p.relative_to(root))]=entry(p)
    return out
for name in ['system','system_ext']:
    expected=inventory(r/'mounts'/name)
    if name=='system':
        for sub in ['my_product','my_stock','my_manifest','my_region','my_engineering','my_carrier','my_heytap','my_bigball']:
            for path,row in inventory(r/'mounts'/sub).items():expected[sub if path=='.' else sub+'/'+path]=row
    actual=inventory(r/'mounts'/('build-'+name))
    # The newly formatted filesystem creates lost+found. An existing donor
    # lost+found is checked normally; otherwise allow only the empty new dir.
    if 'lost+found' not in expected:
        assert not list((r/'mounts'/('build-'+name)/'lost+found').iterdir())
        actual.pop('lost+found')
    assert set(expected)==set(actual),(name,sorted(set(expected)^set(actual)))
    errors=[p for p in expected if expected[p]!=actual[p]]
    assert not errors,(name,errors[:20],[(p,expected[p],actual[p]) for p in errors[:2]])
    results[name]=dict(entries=len(expected),contents_modes_owners_symlinks_xattrs_equal=True)
print(json.dumps(dict(scope='Exact official system/system_ext with same-release OEM directories merged; no TB compatibility modifications, no boot or hardware claim',partitions=results),indent=2))
