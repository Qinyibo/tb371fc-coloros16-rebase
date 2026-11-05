#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/scheduler-compat"
m="$r/speaker-compat/mount-system_ext"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
trap 'mountpoint -q "$m" && umount "$m" || true' EXIT
mount -t ext4 -o loop,rw,noatime "$r/integrated-network/system_ext-stack-v4.img" "$m"
python3 - "$r" "$m" <<'PY'
from pathlib import Path
import os,json,hashlib,sys
r,m=map(Path,sys.argv[1:]);w=r/'scheduler-compat';record=json.loads((w/'integration.json').read_text());sha=lambda b:hashlib.sha256(b).hexdigest()
def replace(rel,data,expected):
 p=m/rel;old=p.read_bytes();assert sha(old)==expected,(rel,sha(old));s=p.stat();a={k:os.getxattr(p,k) for k in os.listxattr(p)};p.write_bytes(data)
 assert (p.stat().st_mode,p.stat().st_uid,p.stat().st_gid)==(s.st_mode,s.st_uid,s.st_gid)
 assert a=={k:os.getxattr(p,k) for k in os.listxattr(p)}
new=(w/'policy/physical-system_ext.cil').read_bytes()+b'\n'+(w/'scheduler.cil').read_bytes()
for item in record['modified']:
 rel=item['path']
 if rel.endswith('system_ext_sepolicy.cil'):data=new
 elif rel.endswith('system_ext_sepolicy_and_mapping.sha256'):data=(sha(new+(m/'etc/selinux/mapping/202504.cil').read_bytes())+'\n').encode()
 else:assert sha((m/rel).read_bytes())==item['after_sha256'];continue
 replace(rel,data,item['after_sha256']);item['after_sha256']=sha(data)
rel='bin/tb371fc-scheduler';data=(w/'build/tb371fc-scheduler').read_bytes();replace(rel,data,record['added'][rel]['sha256']);record['added'][rel]['sha256']=sha(data)
assert sha((m/'priv-app/OplusLauncher/OplusLauncher.apk').read_bytes())=='374c0ffb9b0ff9ef1b8f667a1219611ae6c01d3f973dde00c0527fdbb0a1fd1d'
assert sha((m/'priv-app/Settings/Settings.apk').read_bytes())=='92d419f2df202995b603080a3f3812a57417de3dc4b0eb527e4a3451de112264'
(w/'policy/candidate-system_ext.cil').write_bytes(new)
record['power_api_replaces_generic_sysfs_read']=True;record['exact_candidate_policy_verified']=False;record['physical_verified']=False
(w/'integration.json').write_text(json.dumps(record,indent=2)+'\n')
PY
umount "$m"
e2fsck -fn "$r/integrated-network/system_ext-stack-v4.img" > "$w/system_ext-fsck.log" 2>&1
printf 'NATIVE_POWER_API_INTEGRATED_WITHOUT_SYSFS_READ_GRANT\n'
