#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/ui-compat/native-ui/tablet-profile-v7"
m="$w/mount"
old="$r/integrated-network/system-pad-layout-v5.img"
new="$r/integrated-network/system-tablet-profile-v7.img"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
test ! -e "$new"
test "$(sha256sum "$old" | cut -d' ' -f1)" = a1bb492c93e97017cfd7199dd660099ae856d15d42102053b843471dadd3bd07
cp --reflink=auto --sparse=always "$old" "$new"
mkdir -p "$m"
trap 'if mountpoint -q "$m"; then umount "$m"; fi' EXIT
mount -t ext4 -o loop,rw "$new" "$m"
python3 - "$m" "$w" <<'INNER'
from pathlib import Path
import hashlib,json,os,re,sys,zipfile
m,w=map(Path,sys.argv[1:]);sha=lambda b:hashlib.sha256(b).hexdigest()
changes=[]
def replace(path,after):
 before=path.read_bytes();st=path.stat();attrs={n:os.getxattr(path,n) for n in os.listxattr(path)}
 path.write_bytes(after)
 assert (st.st_uid,st.st_gid,st.st_mode)==(path.stat().st_uid,path.stat().st_gid,path.stat().st_mode)
 assert attrs=={n:os.getxattr(path,n) for n in os.listxattr(path)}
 assert path.read_bytes()==after
 changes.append({'file':str(path.relative_to(m)),'before_sha256':sha(before),'after_sha256':sha(after),'owner_mode_xattrs_unchanged':True})
p=m/'my_product/build.prop';before=p.read_bytes()
assert len(re.findall(rb'^ro\.sf\.lcd_density=360\r?$',before,re.M))==1
after=re.sub(rb'(?m)^ro\.sf\.lcd_density=360(?=\r?$)',b'ro.sf.lcd_density=370',before)
assert after.replace(b'ro.sf.lcd_density=370',b'ro.sf.lcd_density=360')==before
replace(p,after)
p=m/'my_product/overlay/LauncherResourceOverlay/LauncherResourceOverlay.apk'
assert p.read_bytes()==(w/'LauncherResourceOverlay.before.apk').read_bytes()
new=(w/'LauncherResourceOverlay.apk').read_bytes()
with zipfile.ZipFile(p) as a,zipfile.ZipFile(w/'LauncherResourceOverlay.apk') as b:
 assert all(a.read(n)==b.read(n) for n in a.namelist() if n!='resources.arsc' and not n.startswith('META-INF/'))
replace(p,new)
(w/'integration.json').write_text(json.dumps({'changed_files':changes,'density':{'before':360,'after':370},'portrait_native_margin_dp':{'before':133,'after':72},'landscape_native_margin_dp_unchanged':106,'launcher_code_unchanged':True,'extra_overlay_added':False,'runtime_override_added':False,'physical_verified':False},indent=2)+'\n')
print('TWO_NATIVE_CONFIGURATION_FILES_INTEGRATED',flush=True)
INNER
umount "$m"
e2fsck -fn "$new" > "$w/system-fsck.log" 2>&1
printf 'SYSTEM_FILESYSTEM_CHECK_PASS\n'
