#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
base="$r/erofs-lz4-ab/corpus"
out="$r/erofs-lz4-ab/corpus-r2"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
mkdir "$out"
aarch64-linux-gnu-gcc -static -O2 -Wall "$r/erofs_vm_corpus.c" -o "$out/init"
python3 - "$out" <<'PY'
import gzip,pathlib,sys
out=pathlib.Path(sys.argv[1]);buf=bytearray()
for i,(name,mode,data) in enumerate((('init',0o100755,(out/'init').read_bytes()),('TRAILER!!!',0,b'')),1):
 n=name.encode()+b'\0';v=[i,mode,0,0,1,0,len(data),0,0,0,0,len(n),0]
 buf.extend(b'070701'+''.join(f'{x:08x}' for x in v).encode()+n)
 buf.extend(b'\0'*(-len(buf)%4));buf.extend(data);buf.extend(b'\0'*(-len(buf)%4))
(out/'init-override.cpio.gz').write_bytes(gzip.compress(buf,mtime=0))
PY
for archive in "$base"/batch-*.cpio.gz; do
 name="$(basename "$archive" .cpio.gz)"
 cat "$archive" "$out/init-override.cpio.gz" > "$out/current.cpio.gz"
 timeout 95 qemu-system-aarch64 -M virt -cpu cortex-a57 -m 1152 -smp 2 -nographic -no-reboot -nic none -kernel "$r/erofs-runtime-vm/Image" -initrd "$out/current.cpio.gz" -append 'console=ttyAMA0 rdinit=/init panic=-1' > "$out/$name.log" 2>&1
 grep -E '^(BATCH|FAIL|FATAL) ' "$out/$name.log" | tail -5
done
rm "$out/current.cpio.gz"
python3 - "$base" "$out" <<'PY'
import json,pathlib,re,sys
base,out=map(pathlib.Path,sys.argv[1:])
manifest={x['package']:x for x in json.loads((base/'manifest.json').read_text())}
found={}
for p in sorted(out.glob('batch-*.log')):
 s=p.read_text(errors='replace')
 m=re.findall(r'^APEX (\S+) files=(\d+) dirs=(\d+) links=(\d+) bytes=(\d+) random_reads=(\d+) errors=(\d+)$',s,re.M)
 n=re.findall(r'^BATCH packages=(\d+) errors=0$',s,re.M)
 assert n==[str(len(m))] and m and not re.search(r'^FAIL |^FATAL |failed to decompress|Kernel panic|Internal error: Oops',s,re.M),p
 for name,*raw in m:
  f,d,l,b,k,e=map(int,raw);a=manifest[name]
  assert a['batch']==int(p.stem[6:]) and (f,d,l,b,e)==(a['files'],a['dirs'],a['links'],a['bytes'],0) and name not in found,name
  found[name]={**a,'random_reads':k}
assert set(found)==set(manifest) and len(found)==32
result=dict(scope='Virtual ARM64 r107-derived control kernel with corrected EROFS module, original APEX payloads over read-only loop, readahead from cold first open; no dm-verity or physical tablet tested',packages=len(found),totals={k:sum(a[k] for a in found.values()) for k in ('files','dirs','links','bytes','random_reads')},payloads=list(found.values()))
assert result['totals']['random_reads']>5000,result['totals']
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['packages'],result['totals'])
PY
