#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
c="$r/camera-compat-native"
source="$r/mounts/my_product/product_overlay"
img="$r/integrated-network/product-camera.img"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
cp "$r/integrated-network/product.img" "$img"
mkdir -p "$c/mount-product"
trap 'if mountpoint -q "$c/mount-product"; then umount "$c/mount-product"; fi' EXIT
mount -t ext4 -o loop,rw "$img" "$c/mount-product"
python3 - "$c" "$source" <<'PY'
import hashlib,json,os,pathlib,subprocess,sys,xml.etree.ElementTree as ET
work,source=map(pathlib.Path,sys.argv[1:]); dest=work/'mount-product'
name='etc/permissions/com.oplus.camera.unit.sdk_product.xml'
src=source/name; out=dest/name
assert not out.exists() and out.parent.is_dir()
subprocess.run(['cp','-a','--',src,out],check=True)
before=src.read_bytes()
wrong=b'<? xml version = "1.0" encoding = "utf-8" ?>'
right=b'<?xml version="1.0" encoding="utf-8"?>'
assert before.startswith(wrong)
# The SDK JARs already live in the built-in OEM overlay. Register their actual
# paths in product SystemConfig without an overlay mount or duplicate bytes.
normalized=right+before[len(wrong):]
assert normalized.count(b'/product/framework/com.oplus.camera.unit.sdk')==3
updated=normalized.replace(b'/product/framework/com.oplus.camera.unit.sdk',b'/my_product/product_overlay/framework/com.oplus.camera.unit.sdk')
out.write_bytes(updated)
xml=ET.fromstring(out.read_bytes()); assert xml.tag=='permissions'
paths={x.attrib['name']:x.attrib['file'] for x in xml}
assert paths=={
 'com.oplus.camera.unit.sdk':'/my_product/product_overlay/framework/com.oplus.camera.unit.sdk.jar',
 'com.oppo.camera.unit.sdk':'/my_product/product_overlay/framework/com.oplus.camera.unit.sdk.jar',
 'com.oplus.camera.unit.sdk.adapter':'/my_product/product_overlay/framework/com.oplus.camera.unit.sdk.adapter.jar',
 'androidx.camera.extensions.impl':'/system/system_ext/framework/androidx.camera.extensions.impl.jar'}
for path in paths.values():
 if path.startswith('/my_product/'):
  jar=source/'framework'/path.rsplit('/',1)[-1]
  assert jar.is_file() and jar.read_bytes()==(work/jar.name).read_bytes()
assert out.stat().st_uid==src.stat().st_uid==0 and out.stat().st_gid==src.stat().st_gid==0 and (out.stat().st_mode&0o777)==0o644
assert os.getxattr(out,'security.selinux')==os.getxattr(src,'security.selinux')==b'u:object_r:system_file:s0'
changes={name:{'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'library_paths':paths}}
(work/'product-camera-files.json').write_text(json.dumps(changes,indent=2)+'\n')
PY
umount "$c/mount-product"
e2fsck -fn "$img" > "$c/product-camera-fsck.log" 2>&1
printf '%s\n' CAMERA_DONOR_LIBRARIES_INTEGRATED_PRODUCT_FSCK_PASS
