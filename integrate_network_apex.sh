#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
base="$r/integrated-logicals"
out="$r/integrated-network"
a="$r/bpf-compat/rebuilt-tethering"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
mkdir "$out"; mkdir "$out/old" "$out/new"
cleanup() { for d in old new; do if mountpoint -q "$out/$d"; then umount "$out/$d"; fi; done; }
trap cleanup EXIT
for f in system_ext.img product.img runtime-sepolicy; do ln "$base/$f" "$out/$f"; done
cp --reflink=auto --sparse=always "$base/system.img" "$out/system.img"
mount -t ext4 -o rw,loop "$out/system.img" "$out/new"
p="$out/new/system/apex/com.android.tethering.apex"
python3 - "$a" "$p" <<'PY'
import hashlib,json,pathlib,sys
r,p=map(pathlib.Path,sys.argv[1:]);d=json.loads((r/'result.json').read_text()); image=(r/'com.android.tethering.apex').read_bytes()
assert hashlib.sha256(p.read_bytes()).hexdigest()==d['official_sha256']
assert hashlib.sha256(image).hexdigest()==d['sha256']
assert not p.with_name(p.name+'.fsv_meta').exists()
with p.open('wb') as f:f.write(image)
PY
sync -f "$out/new"; umount "$out/new"
e2fsck -fn "$out/system.img" > "$out/fsck-system.log" 2>&1
mount -t ext4 -o ro,noload,loop "$base/system.img" "$out/old"
mount -t ext4 -o ro,noload,loop "$out/system.img" "$out/new"
python3 - "$r" "$out" "$a" <<'PY'
import hashlib,json,pathlib,sys
r,out,apex=map(pathlib.Path,sys.argv[1:]); ns={};exec((r/'verify_base.py').read_text().split("for name in ['system','system_ext']:")[0],ns)
a,b=(ns['inventory'](out/tag) for tag in ('old','new')); k='system/apex/com.android.tethering.apex'
assert a.keys()==b.keys()
assert {x for x in a if a[x]!=b[x]}=={k}
assert {i:v for i,v in a[k].items() if i not in ('size','sha256')}=={i:v for i,v in b[k].items() if i not in ('size','sha256')}
assert b[k]['sha256']==json.loads((apex/'result.json').read_text())['sha256']
(out/'tree-verification.json').write_text(json.dumps(dict(entries=len(b),only_delta=k,old_sha256=a[k]['sha256'],new_sha256=b[k]['sha256'],metadata_unchanged=True),indent=2)+'\n')
print('INTEGRATED_SYSTEM_APEX_ONLY_DELTA_PASS',len(b),flush=True)
PY
cleanup
sha256sum "$out/system.img" > "$out/SHA256SUMS"
for f in system_ext.img product.img runtime-sepolicy; do test "$out/$f" -ef "$base/$f"; sed -n "s@ $base/$f\$@ $out/$f@p" "$base/SHA256SUMS" >> "$out/SHA256SUMS"; done
python3 "$r/build_integrated_super.py" "$r" --network
