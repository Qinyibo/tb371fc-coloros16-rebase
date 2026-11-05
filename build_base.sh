#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
out="$r/base-ext4-UNADAPTED"
test ! -e "$out"
mkdir -p "$out" "$r/mounts/build-system" "$r/mounts/build-system_ext"
cleanup() {
 for n in system system_ext; do
  if mountpoint -q "$r/mounts/build-$n"; then umount "$r/mounts/build-$n"; fi
 done
}
trap cleanup EXIT
opts='^has_journal,^64bit,^metadata_csum,^flex_bg,^resize_inode,ext_attr,dir_index,filetype,extent,sparse_super,large_file,huge_file,uninit_bg,dir_nlink,extra_isize'
make_image() {
 local n=$1 size=$2
 truncate -s "$size" "$out/$n.img"
 mke2fs -q -F -t ext4 -b 4096 -I 256 -L "$n" -m 0 -N 32768 -O "$opts" "$out/$n.img"
 mount -t ext4 -o loop,rw "$out/$n.img" "$r/mounts/build-$n"
 rsync -aHAX --numeric-ids "$r/mounts/$n/" "$r/mounts/build-$n/"
}
make_image system 10187964416
for n in my_product my_stock my_manifest my_region my_engineering my_carrier my_heytap my_bigball; do
 rsync -aHAX --numeric-ids "$r/mounts/$n/" "$r/mounts/build-system/$n/"
done
echo SYSTEM_CONTENT_COPIED
make_image system_ext 1702887424
# VNDK30 is an explicitly separate compatibility input. Stage it separately
# until its signing/namespace/SELinux contract has been checked; don't silently
# mix it into the official base conversion.
sync
cleanup
bash "$r/resume_base.sh"
