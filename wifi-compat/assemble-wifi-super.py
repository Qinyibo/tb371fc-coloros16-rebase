import hashlib
import json
from pathlib import Path
import shutil
import struct

root=Path(__file__).resolve().parent.parent
work=root/'wifi-compat'
base=root/'integrated-network'
info=json.loads((work/'delta-result.json').read_text())
layout=json.loads((base/'super-result.json').read_text())
assert info['base_super_sha256']==json.loads((root/'qspm-compat/delta-result.json').read_text())['updated_super_sha256']
source=base/'super-cleanbase-qspm-OFFLINE.img'
target=base/'super-cleanbase-wifi-OFFLINE.img'
tmp=target.with_suffix('.img.partial')
assert not target.exists() and not tmp.exists()
shutil.copyfile(source,tmp)
assert tmp.stat().st_size==layout['bytes']
part=layout['logical_partitions']['system_a']
low=part['start_sector']*512
high=low+part['bytes']
changed=0
with tmp.open('r+b') as dst:
    for member in info['parts']:
        path=work/member['file']; data=path.read_bytes()
        assert hashlib.sha256(data).hexdigest()==member['sha256']
        magic,major,minor,header_size,chunk_size,block,total,count,crc=struct.unpack_from('<IHHHHIIII',data)
        assert (magic,major,minor,header_size,chunk_size,block,total*block,crc)==(0xed26ff3a,1,0,28,12,4096,layout['bytes'],0)
        offset=header_size; location=0
        for index in range(count):
            kind,pad,blocks,length=struct.unpack_from('<HHII',data,offset); size=blocks*block
            assert pad==0 and size>0
            if kind==0xcac1:
                assert length==chunk_size+size and low<=location<location+size<=high
                dst.seek(location)
                dst.write(data[offset+chunk_size:offset+length]); changed+=size
            else:
                assert kind==0xcac3 and length==chunk_size
            location+=size; offset+=length
        assert location==layout['bytes'] and offset==len(data)
assert changed==info['changed_raw_bytes']
with tmp.open('rb') as f: actual=hashlib.file_digest(f,'sha256').hexdigest()
assert actual==info['updated_super_sha256']
tmp.rename(target)
print('STANDALONE_WIFI_SUPER_FULL_HASH_PASS',actual,flush=True)
