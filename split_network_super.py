import hashlib
import json
from pathlib import Path
import struct

root = Path(__file__).resolve().parent / 'flash-network-candidate'
entry = next(r for r in json.loads((root/'manifest.json').read_text())['images'] if r['name']=='super')
source = root / entry['path']
out = root / 'super-parts-32m'
out.mkdir(exist_ok=False)
block = 4096
file_header = struct.Struct('<IHHHHIIII')
chunk_header = struct.Struct('<HHII')
max_encoded = 32 << 20
payload_limit = (max_encoded - file_header.size - 3 * chunk_header.size) // block * block
total_blocks = entry['bytes'] // block
assert total_blocks * block == entry['bytes'] == source.stat().st_size

def chunk(kind, count, length=0):
    return chunk_header.pack(kind, 0, count, chunk_header.size+length)

digest = hashlib.sha256()
rows = []
with source.open('rb') as src:
    for start in range(0, entry['bytes'], payload_limit):
        size = min(payload_limit, entry['bytes']-start)
        data = src.read(size)
        assert len(data) == size
        digest.update(data)
        start_block, count = start//block, size//block
        gap_after = total_blocks-start_block-count
        pieces = [file_header.pack(0xed26ff3a,1,0,file_header.size,chunk_header.size,block,total_blocks,1+bool(start)+bool(gap_after),0)]
        if start_block:
            pieces.append(chunk(0xcac3,start_block))
        pieces += [chunk(0xcac1,count,size),data]
        if gap_after:
            pieces.append(chunk(0xcac3,gap_after))
        part = b''.join(pieces)
        name = f'super.part{len(rows):04d}.sparse.img'
        assert len(part) <= max_encoded
        with (out/name).open('xb') as dest:
            dest.write(part)
        rows.append(dict(file=name,size=len(part),sha256=hashlib.sha256(part).hexdigest(),start=start,raw_bytes=size))
        if len(rows)%64==0:
            print('PARTS_WRITTEN',len(rows),flush=True)
    assert not src.read(1)
assert digest.hexdigest() == entry['sha256']
receipt = dict(format='android-sparse-contiguous-exact-v1',source_sha256=digest.hexdigest(),expanded_size=entry['bytes'],max_part_size=max_encoded,parts=rows)
(out/'manifest.json.tmp').write_text(json.dumps(receipt,indent=2)+'\n',encoding='ascii')
(out/'manifest.json.tmp').rename(out/'manifest.json')
print('SUPER_EXACT_SPARSE_PARTS_READY',len(rows),digest.hexdigest(),flush=True)
