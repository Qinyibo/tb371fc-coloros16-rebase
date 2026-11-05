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
import os,sys,stat,hashlib,json
r,m=map(Path,sys.argv[1:]);w=r/'scheduler-compat';sha=lambda b:hashlib.sha256(b).hexdigest()
assert not (w/'integration.json').exists()
assert json.loads((w/'policy/result.json').read_text())['scheduler_own_neverallow_failures']==0
assert 'NATIVE_LIFECYCLE_FAILURES=0' in (w/'tests/lifecycle.log').read_text()
assert sha((m/'priv-app/OplusLauncher/OplusLauncher.apk').read_bytes())=='374c0ffb9b0ff9ef1b8f667a1219611ae6c01d3f973dde00c0527fdbb0a1fd1d'
def tree():
 result={}
 for base,dirs,files in os.walk(m,followlinks=False):
  for name in dirs+files:
   p=Path(base)/name;s=p.lstat();v={'mode':s.st_mode,'uid':s.st_uid,'gid':s.st_gid,'xattrs':{k:os.getxattr(p,k,follow_symlinks=False).hex() for k in os.listxattr(p,follow_symlinks=False)}}
   if stat.S_ISREG(s.st_mode):v['sha256']=sha(p.read_bytes())
   elif stat.S_ISLNK(s.st_mode):v['target']=os.readlink(p)
   result[str(p.relative_to(m))]=v
 return result
before=tree();changes=[]
def replace(rel,data):
 p=m/rel;original=p.read_bytes();st=p.stat();attrs={k:os.getxattr(p,k) for k in os.listxattr(p)};p.write_bytes(data)
 assert (p.stat().st_mode,p.stat().st_uid,p.stat().st_gid)==(st.st_mode,st.st_uid,st.st_gid)
 assert attrs=={k:os.getxattr(p,k) for k in os.listxattr(p)}
 changes.append({'path':rel,'before_sha256':sha(original),'after_sha256':sha(data)})
rel='etc/selinux/system_ext_sepolicy.cil';old=(m/rel).read_bytes()
assert sha(old)=='561086e631499c7b7f5dbe96003951874a999db7b2e09e6783e9e52a6c9f1964'
assert b'tb371fc_scheduler' not in old
new=old+b'\n'+(w/'scheduler.cil').read_bytes();replace(rel,new);(w/'policy/candidate-system_ext.cil').write_bytes(new)
rel='etc/selinux/system_ext_file_contexts';old=(m/rel).read_bytes();assert b'tb371fc_scheduler' not in old
replace(rel,old+b'\n'+(w/'file_contexts.add').read_bytes())
# Original OEM hash exactly equals SHA256(CIL || mapping/202504.cil).
assert json.loads((w/'policy/hash-recipe.json').read_text())['exact_matching_current_api_mappings']==['202504.cil']
replace('etc/selinux/system_ext_sepolicy_and_mapping.sha256',(sha(new+(m/'etc/selinux/mapping/202504.cil').read_bytes())+'\n').encode())
for rel,src,mode,context in [('bin/tb371fc-scheduler',w/'build/tb371fc-scheduler',0o755,'tb371fc_scheduler_exec'),('etc/init/tb371fc-scheduler.rc',w/'tb371fc-scheduler.rc',0o644,'system_file')]:
 p=m/rel;assert not p.exists();p.write_bytes(src.read_bytes());os.chmod(p,mode);os.chown(p,0,0);os.setxattr(p,'security.selinux',('u:object_r:'+context+':s0').encode())
after=tree();removed=set(before)-set(after);added=set(after)-set(before);changed={k for k in before if k in after and before[k]!=after[k]}
assert not removed and added=={'bin/tb371fc-scheduler','etc/init/tb371fc-scheduler.rc'}
assert changed=={'etc/selinux/system_ext_sepolicy.cil','etc/selinux/system_ext_file_contexts','etc/selinux/system_ext_sepolicy_and_mapping.sha256'},changed
(w/'integration.json').write_text(json.dumps({'status':'INTEGRATED_OFFLINE_RUNTIME_PENDING','all_other_tree_entries_unchanged':True,'existing_entries':len(before),'modified':changes,'added':{k:after[k] for k in added},'removed':[],'magisk_dependency_added':False,'physical_verified':False},indent=2)+'\n')
PY
umount "$m"
e2fsck -fn "$r/integrated-network/system_ext-stack-v4.img" > "$w/system_ext-fsck.log" 2>&1
printf 'NATIVE_SCHEDULER_FIVE_FILE_BOUNDARY_AND_FILESYSTEM_VERIFIED\n'
