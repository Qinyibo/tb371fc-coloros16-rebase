"""Read full OTA operations with field numbers checked against update_metadata.proto."""
import base64,bz2,collections,hashlib,json,lzma,pathlib,struct,sys,zipfile
ROOT=pathlib.Path(__file__).resolve().parent
def wire(b):
    out=collections.defaultdict(list);p=0
    def var():
        nonlocal p
        n=s=0
        while True:
            v=b[p];p+=1;n|=(v&127)<<s;s+=7
            if v<128:return n
            assert s<=70
    while p<len(b):
        tag=var();f,t=tag>>3,tag&7
        if t==0:v=var()
        elif t==2:n=var();v=b[p:p+n];p+=n
        elif t in (1,5):n=8 if t==1 else 4;v=int.from_bytes(b[p:p+n],'little');p+=n
        else:raise ValueError(t)
        out[f].append(v)
    assert p==len(b)
    return out
def one(d,f,default=None):return d[f][0] if d.get(f) else default
def main():
    manifest=wire((ROOT/'payload-manifest.pb').read_bytes())
    parts={one(wire(b),1).decode():wire(b) for b in manifest[13]}
    summary={'minor_version':one(manifest,12,0),'partial_update':one(manifest,16,0),'block_size':one(manifest,3,4096),'partitions':[]}
    for name,p in parts.items():
        ni=wire(one(p,7));ops=[wire(b) for b in p[8]]
        summary['partitions'].append(dict(name=name,bytes=one(ni,1),sha256=one(ni,2).hex(),old_partition_info=bool(p.get(6)),operations=dict(collections.Counter(one(o,1) for o in ops))))
    (ROOT/'partition-inventory.json').write_text(json.dumps(summary,indent=2))
    if len(sys.argv)==1:
        print(json.dumps(summary,indent=2));sys.exit()
    # OEM emits minor=9/partial_update=1 even here. Prove self-containment
    # from actual operations and absent old image information, not a version flag.
    assert all(not row['old_partition_info'] and set(map(int,row['operations'])) <= {0,1,6,7,8} for row in summary['partitions'])
    archive=ROOT/'original/OPD2413_16.0.10.600_CN01.zip'
    header=json.loads((ROOT/'payload-header.json').read_text());data_start=24+header['manifest_length']+header['metadata_signature_length'];bs=summary['block_size']
    outdir=ROOT/'donor-images';outdir.mkdir(exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        props=dict(line.split('=',1) for line in z.read('payload_properties.txt').decode().splitlines())
        with z.open('payload.bin') as stream:
            h=hashlib.sha256();n=0;mh=hashlib.sha256()
            while b:=stream.read(16<<20):
                h.update(b)
                if n<int(props['METADATA_SIZE']):mh.update(b[:int(props['METADATA_SIZE'])-n])
                n+=len(b)
        assert n==int(props['FILE_SIZE']) and base64.b64encode(h.digest()).decode()==props['FILE_HASH']
        assert base64.b64encode(mh.digest()).decode()==props['METADATA_HASH']
        print('PAYLOAD_HASHES_PASS',flush=True)
        (ROOT/'payload-hash-result.json').write_text(json.dumps(dict(bytes=n,file_hash_pass=True,metadata_hash_pass=True),indent=2))
    # Direct raw ZIP access: payload is stored, not deflated.
    with archive.open('rb') as source:
        for row in summary['partitions']:
            name=row['name']
            if name not in sys.argv[1:] and 'all' not in sys.argv[1:]:continue
            target=outdir/(name+'.img');assert not target.exists(),target
            temp=target.with_suffix('.partial')
            with temp.open('wb') as out:
                out.truncate(row['bytes'])
                for raw in parts[name][8]:
                    o=wire(raw);typ=one(o,1);assert typ in (0,1,6,7,8),typ
                    length=one(o,3,0);source.seek(header['offset']+data_start+one(o,2,0));b=source.read(length);assert len(b)==length
                    if length and o.get(8):assert hashlib.sha256(b).digest()==one(o,8)
                    if typ==1:b=bz2.decompress(b)
                    elif typ==8:b=lzma.decompress(b)
                    elif typ in (6,7):b=b''
                    cursor=0
                    for eb in o[6]:
                        e=wire(eb);pos=one(e,1)*bs;count=one(e,2)*bs
                        assert pos+count<=row['bytes']
                        if typ not in (6,7):
                            assert len(b[cursor:cursor+count])==count
                            out.seek(pos);out.write(b[cursor:cursor+count]);cursor+=count
                    if typ not in (6,7):assert cursor==len(b)
            with temp.open('rb') as inp:actual=hashlib.file_digest(inp,'sha256').hexdigest()
            assert actual==row['sha256'],(name,actual,row['sha256'])
            temp.rename(target);print('PARTITION_HASH_PASS',name,row['bytes'],flush=True)

if __name__ == "__main__": main()
