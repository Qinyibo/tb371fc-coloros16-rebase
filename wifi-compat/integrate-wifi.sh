#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/wifi-compat";img="$r/integrated-network/system-wifi.img"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
test ! -e "$img"
cp --reflink=auto --sparse=always "$r/integrated-network/system-qspm.img" "$img"
mkdir -p "$w/mount-system"
trap 'if mountpoint -q "$w/mount-system"; then umount "$w/mount-system"; fi' EXIT
mount -t ext4 -o loop,rw "$img" "$w/mount-system"
python3 - "$w" <<'PY'
import pathlib,os,hashlib,json,sys
w=pathlib.Path(sys.argv[1]);root=w/'mount-system';p=root/'system/apex/com.android.wifi.apex';info=json.loads((w/'rebuilt-wifi/result.json').read_text());old=p.read_bytes();new=(w/'rebuilt-wifi/com.android.wifi.apex').read_bytes()
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(old)==info['official_sha256'] and sha(new)==info['sha256'] and not p.with_name(p.name+'.fsv_meta').exists()
st=p.stat();attrs={n:os.getxattr(p,n) for n in os.listxattr(p)}
p.write_bytes(new)
assert (p.stat().st_mode,p.stat().st_uid,p.stat().st_gid)==(st.st_mode,st.st_uid,st.st_gid) and attrs=={n:os.getxattr(p,n) for n in os.listxattr(p)}
assert sha((root/'system/framework/oplus-services.jar').read_bytes())=='d17d7bfc4d0a0d8adc1a0b1147fa2aa5ff9f6d21f33513689e9ea7f7190c3737'
(w/'system-integration.json').write_text(json.dumps({'changed_file':str(p.relative_to(root)),'before':sha(old),'after':sha(new),'qspm_guard_preserved':True,'metadata_preserved':True,'camera_or_display_changes_included':False},indent=2)+'\n')
PY
umount "$w/mount-system"
e2fsck -fn "$img" > "$w/system-wifi-fsck.log" 2>&1
echo WIFI_APEX_INTEGRATED_QSPM_GUARD_PRESERVED_FSCK_PASS
