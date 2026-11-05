import json,pathlib,struct,sys,zipfile
r=pathlib.Path(sys.argv[1]);rows=[]
for directory in ['system/system/apex','system_ext/apex','product/apex','my_product/apex']:
 for p in sorted((r/'mounts'/directory).glob('*.apex')):
  with zipfile.ZipFile(p) as z:
   i=z.getinfo('apex_payload.img')
   with z.open(i) as f:header=f.read(1152)
  erofs=struct.unpack_from('<I',header,1024)[0]==0xe0f5e1e2
  ext4=struct.unpack_from('<H',header,1080)[0]==0xef53
  row=dict(package=str(p.relative_to(r/'mounts')),payload_bytes=i.file_size,filesystem='erofs' if erofs else 'ext4' if ext4 else 'unknown')
  if erofs:row.update(block_bits=header[1036],feature_compat=struct.unpack_from('<I',header,1032)[0],feature_incompat=struct.unpack_from('<I',header,1104)[0],compression_mask=struct.unpack_from('<H',header,1108)[0])
  rows.append(row)
(r/'apex-filesystem-inventory.json').write_text(json.dumps(rows,indent=2))
from collections import Counter
print('APEX_FILESYSTEMS',dict(Counter(x['filesystem'] for x in rows)))
print('EROFS_VARIANTS',dict(Counter((x['feature_incompat'],x['compression_mask'],x['block_bits']) for x in rows if x['filesystem']=='erofs')))
