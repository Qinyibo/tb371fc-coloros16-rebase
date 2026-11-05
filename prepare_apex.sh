#!/bin/bash
set -eu
r=/mnt/d/TB371FC-release/clean-rebase-20261104
export PYTHONDONTWRITEBYTECODE=1
python3 - "$r" <<'PY'
import json,pathlib,sys,zipfile,hashlib
r=pathlib.Path(sys.argv[1]);rows=[]
sources={'com.android.runtime':r/'mounts/system/system/apex/com.android.runtime.apex','com.android.vndk.v30':r/'tb-readback/com.android.vndk.v30.apex'}
for name,source in sources.items():
 out=r/'apex-inputs'/name;out.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(source) as z:
  for member in ['apex_payload.img','apex_pubkey','apex_manifest.pb']:
   target=out/member
   if not target.exists():
    with z.open(member) as src,target.open('wb') as dst:
     while b:=src.read(8<<20):dst.write(b)
  assert z.testzip() is None
 with source.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
 rows.append(dict(name=name,source=str(source),sha256=digest))
(r/'apex-inputs/source.json').write_text(json.dumps(rows,indent=2))
PY
for n in com.android.runtime com.android.vndk.v30; do
 mkdir -p "$r/mounts/$n"
 if ! mountpoint -q "$r/mounts/$n"; then mount -o ro,loop "$r/apex-inputs/$n/apex_payload.img" "$r/mounts/$n"; fi
done
ls "$r/mounts/tb-vendor/bin/hw" | grep -E 'camera|composer|audio|sensors|power'
