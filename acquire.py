import concurrent.futures, hashlib, io, json, pathlib, struct, time, zipfile
import requests

ROOT = pathlib.Path(__file__).resolve().parent
info = json.loads((ROOT/'link-result.json').read_text())
url = info['url']
size = int(info['headers']['Content-Length'])

def get_range(start, end):
    r = requests.get(url, headers={'Range': f'bytes={start}-{end}', 'Accept-Encoding':'identity'}, timeout=(20,120))
    r.raise_for_status()
    assert r.status_code == 206 and len(r.content) == end-start+1, (r.status_code,len(r.content),start,end)
    return r.content

class Remote(io.RawIOBase):
    def __init__(self): self.pos=0
    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos
    def seek(self, offset, whence=0):
        self.pos = offset if whence==0 else self.pos+offset if whence==1 else size+offset
        return self.pos
    def read(self, n=-1):
        end=size if n<0 else min(size,self.pos+n)
        if end<=self.pos: return b''
        b=get_range(self.pos,end-1); self.pos=end; return b

with zipfile.ZipFile(Remote()) as z:
    (ROOT/'zip-inventory.json').write_text(json.dumps([dict(name=i.filename,size=i.file_size,compressed=i.compress_size,method=i.compress_type,offset=i.header_offset) for i in z.infolist()],indent=2))
    for i in z.infolist():
        if i.file_size < 8*1024*1024 and i.filename != 'payload.bin':
            p=ROOT/'metadata'/i.filename; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(z.read(i))
    i=z.getinfo('payload.bin'); assert i.compress_type==0
    head=get_range(i.header_offset,i.header_offset+29)
    offset=i.header_offset+30+sum(struct.unpack_from('<HH',head,26))
    head=get_range(offset,offset+23)
    magic,version,manifest_len,sig_len=struct.unpack('>4sQQI',head)
    assert magic==b'CrAU' and version==2
    (ROOT/'payload-header.json').write_text(json.dumps(dict(offset=offset,version=version,manifest_length=manifest_len,metadata_signature_length=sig_len),indent=2))
    (ROOT/'payload-manifest.pb').write_bytes(get_range(offset+24,offset+23+manifest_len))
print('METADATA_SAVED',flush=True)

target=ROOT/'original'/'OPD2413_16.0.10.600_CN01.zip.partial'
target.parent.mkdir(exist_ok=True)
assert not target.with_suffix('').exists(), 'Original already exists'
chunk=32*1024*1024
parts=ROOT/'download-parts';parts.mkdir(exist_ok=True)
def fetch(n):
    start=n*chunk; end=min(size,start+chunk)-1;p=parts/f'{n:04}.part'
    if p.exists() and p.stat().st_size==end-start+1: return
    for attempt in range(3):
        try: p.write_bytes(get_range(start,end));return
        except Exception:
            if attempt==2: raise
            time.sleep(2)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    list(pool.map(fetch,range((size+chunk-1)//chunk)))
md5=hashlib.md5();sha=hashlib.sha256()
with target.open('wb') as out:
    for n in range((size+chunk-1)//chunk):
        p=parts/f'{n:04}.part';b=p.read_bytes();out.write(b);md5.update(b);sha.update(b)
assert target.stat().st_size==size
assert md5.hexdigest()==info['headers']['x-amz-meta-filemd5']
target.rename(target.with_suffix(''))
(ROOT/'original-receipt.json').write_text(json.dumps(dict(source=url.split('?')[0],bytes=size,md5=md5.hexdigest(),sha256=sha.hexdigest(),server_headers=info['headers']),indent=2))
print('DOWNLOAD_VERIFIED',size,md5.hexdigest(),sha.hexdigest(),flush=True)
for p in parts.glob('*.part'): p.unlink()
