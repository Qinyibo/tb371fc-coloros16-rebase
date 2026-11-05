import hashlib,importlib.util,json,pathlib
root=pathlib.Path(__file__).resolve().parent
repo=pathlib.Path('D:/TB371FC-release/public-source/TB371FC-ColorOS16')
spec=importlib.util.spec_from_file_location('lp',repo/'rom-build/tools/lp_probe.py');lp=importlib.util.module_from_spec(spec);spec.loader.exec_module(lp)
base=pathlib.Path('D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE')
manifest=json.loads((base/'manifest.json').read_text(encoding='utf-8-sig'));expected={r['name']:r for r in manifest['logical_partitions']}
out=root/'tb-inputs';out.mkdir(exist_ok=True)
with (base/'images/super-R94.img').open('rb') as source:
    head=source.read(2<<20);meta=lp.parse_metadata(head,lp.parse_geometry(head))
    (root/'tb-super-layout.json').write_text(json.dumps(meta,indent=2))
    for p in meta['partitions']:
        if p['name'] not in ('vendor_a','odm_a'):continue
        target=out/(p['name']+'.img')
        if target.exists() and target.stat().st_size==0:target.unlink()
        assert not target.exists()
        h=hashlib.sha256()
        with target.open('wb') as dest:
            for e in p['extents']:
                assert e['source']==e['type']==0
                source.seek(e['target_data']*512);left=e['sectors']*512
                while left:
                    b=source.read(min(left,16<<20));assert b;dest.write(b);h.update(b);left-=len(b)
        assert h.hexdigest()==expected[p['name']]['sha256']
        print('TB_INPUT_HASH_PASS',p['name'],h.hexdigest(),flush=True)
(out/'source.json').write_text(json.dumps(dict(package=str(base),scope='vendor/odm only; v27 boot is r106, not current r107',partitions={k:v for k,v in expected.items() if k in ('vendor_a','odm_a')}),indent=2))
