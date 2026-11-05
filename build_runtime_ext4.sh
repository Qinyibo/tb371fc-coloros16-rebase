#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
out="$r/apex-ext4-prototype/com.android.runtime"
src="$r/mounts/com.android.runtime"
mnt="$r/mounts/runtime-ext4-prototype"
test ! -e "$out"
mkdir -p "$out" "$mnt"
cleanup() { if mountpoint -q "$mnt"; then umount "$mnt"; fi; }
trap cleanup EXIT
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
truncate -s 14680064 "$out/filesystem.img"
mke2fs -q -F -t ext4 -b4096 -I256 -m0 -N512 -L runtime \
 -O '^has_journal,^64bit,^metadata_csum,^flex_bg,^resize_inode,ext_attr,dir_index,filetype,extent,sparse_super,large_file,huge_file,uninit_bg,dir_nlink,extra_isize' "$out/filesystem.img"
mount -t ext4 -o loop,rw "$out/filesystem.img" "$mnt"
rsync -aHAX --numeric-ids "$src/" "$mnt/"
if test ! -e "$src/lost+found"; then rmdir "$mnt/lost+found"; fi
python3 "$r/verify_apex_tree.py" "$src" "$mnt" "$out" prepare
cleanup
debugfs -w -f "$out/symlink-modes.debugfs" "$out/filesystem.img" > "$out/symlink-modes.log" 2>&1
e2fsck -fn "$out/filesystem.img" > "$out/fsck.log" 2>&1
mount -t ext4 -o loop,ro "$out/filesystem.img" "$mnt"
python3 "$r/verify_apex_tree.py" "$src" "$mnt" "$out" verify
cleanup
sha256sum "$out/filesystem.img" > "$out/filesystem.sha256"
echo RUNTIME_EXT4_FILESYSTEM_VERIFIED_NOT_YET_SIGNED
