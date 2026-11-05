#!/bin/bash
set -eu
r=/mnt/d/TB371FC-release/clean-rebase-20261104
for n in system_ext product my_product my_stock my_manifest my_region my_engineering my_carrier my_heytap my_bigball vendor odm; do
 mkdir -p "$r/mounts/$n"
 if ! mountpoint -q "$r/mounts/$n"; then mount -t erofs -o ro,loop "$r/donor-images/$n.img" "$r/mounts/$n"; fi
done
python3 - "$r" <<'PY'
import os,pathlib,json,sys,stat
r=pathlib.Path(sys.argv[1]);rows={}
for tree in (r/'mounts').iterdir():
 size=0;count=0
 for parent,dirs,files in os.walk(tree,followlinks=False):
  for n in dirs+files:
   s=os.lstat(os.path.join(parent,n));count+=1
   if stat.S_ISREG(s.st_mode):size+=(s.st_size+4095)//4096*4096
 rows[tree.name]=dict(data_blocks_bytes=size,entries=count)
(r/'base-size-estimate.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
PY
