import hashlib
import json
from pathlib import Path
import struct

root = Path(__file__).resolve().parent.parent
work = root / 'wifi-compat'
base = root / 'integrated-network'
reference = json.loads((base/'super-result.json').read_text())
qspm=json.loads((root/'qspm-compat/delta-result.json').read_text())
reference['sha256']=qspm['updated_super_sha256']
system = reference['logical_partitions']['system_a']
system['sha256']=qspm['updated_system_sha256']
block = 4096
start = system['start_sector'] * 512
size = system['bytes']
assert start%block == size%block == reference['bytes']%block == 0
old_super = hashlib.sha256()
new_super = hashlib.sha256()
old_system = hashlib.sha256()
new_system = hashlib.sha256()
runs = []

with (base/'super-cleanbase-qspm-OFFLINE.img').open('rb') as old, (base/'system-wifi.img').open('rb') as new:
    def unchanged(size):
        while size:
            chunk = old.read(min(size, 16<<20))
            assert chunk
            old_super.update(chunk)
            new_super.update(chunk)
            size -= len(chunk)

    unchanged(start)
    for off in range(0, size, 16<<20):
        length = min(16<<20, size-off)
        before, after = old.read(length), new.read(length)
        assert len(before) == len(after) == length
        old_super.update(before)
        new_super.update(after)
        old_system.update(before)
        new_system.update(after)
        if before == after:
            continue
        for index in range(0, length, block):
            payload = after[index:index+block]
            if before[index:index+block] == payload:
                continue
            absolute = (start + off + index) // block
            if runs and runs[-1][0] + len(runs[-1][1])//block == absolute:
                runs[-1][1].extend(payload)
            else:
                runs.append((absolute, bytearray(payload)))
    unchanged(reference['bytes']-start-size)
    assert not old.read(1) and not new.read(1)
assert old_super.hexdigest() == reference['sha256'] and old_system.hexdigest() == system['sha256']
assert runs
limit = 32<<20
header = struct.Struct('<IHHHHIIII')
chunk = struct.Struct('<HHII')
span = reference['bytes']//block
parts = []

def write_part(group):
    out = bytearray()
    cursor = 0
    count = 0
    for offset, payload in group:
        if cursor < offset:
            out.extend(chunk.pack(0xcac3,0,offset-cursor,chunk.size)); count+=1
        blocks = len(payload)//block
        out.extend(chunk.pack(0xcac1,0,blocks,chunk.size+len(payload)))
        out.extend(payload); count+=1
        cursor = offset+blocks
    if cursor < span:
        out.extend(chunk.pack(0xcac3,0,span-cursor,chunk.size)); count+=1
    data = header.pack(0xed26ff3a,1,0,header.size,chunk.size,block,span,count,0)+out
    assert len(data)<=limit
    path=work/f'super-wifi-delta-{len(parts):02d}.img'
    with path.open('xb') as f: f.write(data)
    parts.append(dict(file=path.name,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)))

group=[]
encoded=header.size+chunk.size
for offset,payload in runs:
    for off in range(0,len(payload),16<<20):
        section=payload[off:off+(16<<20)]
        extra=2*chunk.size+len(section)
        if group and encoded+extra>limit:
            write_part(group);group=[];encoded=header.size+chunk.size
        group.append((offset+off//block,section));encoded+=extra
write_part(group)
result=dict(base_super_sha256=old_super.hexdigest(),updated_super_sha256=new_super.hexdigest(),updated_system_sha256=new_system.hexdigest(),absolute_changed_range_count=len(runs),changed_raw_bytes=sum(len(data) for _,data in runs),scope='All changed raw blocks belong to system_a; LP metadata and all other partitions identical',parts=parts)
(work/'delta-result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='ascii')
print('SYSTEM_ONLY_SPARSE_DELTA_READY',json.dumps(result),flush=True)
