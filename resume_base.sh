#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
out="$r/base-ext4-UNADAPTED"
cleanup() { for n in system system_ext; do if mountpoint -q "$r/mounts/build-$n"; then umount "$r/mounts/build-$n"; fi; done; }
trap cleanup EXIT
for n in system system_ext; do mount -t ext4 -o ro,loop "$out/$n.img" "$r/mounts/build-$n"; done
python3 "$r/fix_symlink_modes.py" "$r"
cleanup
for n in system system_ext; do
 debugfs -w -f "$out/$n-symlink-modes.debugfs" "$out/$n.img" > "$out/$n-symlink-modes.log" 2>&1
 e2fsck -fn "$out/$n.img" > "$out/fsck-$n.log" 2>&1
 mount -t ext4 -o ro,loop "$out/$n.img" "$r/mounts/build-$n"
done
python3 "$r/verify_base.py" "$r" > "$out/content-verification.json"
cleanup
sha256sum "$out/system.img" "$out/system_ext.img" > "$out/SHA256SUMS"
printf '%s\n' 'OFFICIAL_CONTENT_EXT4_CONVERSION_ONLY_NOT_BOOTABLE_TB_CANDIDATE' > "$out/STATE"
echo BASE_EXT4_CONTENT_METADATA_FSCK_PASS
