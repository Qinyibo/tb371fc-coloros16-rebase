#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
m="$r/speaker-compat/mount-system_ext"
trap 'mountpoint -q "$m" && umount "$m" || true' EXIT
mount -t ext4 -o loop,rw "$r/integrated-network/system_ext-hwprofile.img" "$m"
# Replace only the checked source wrapper; keep all inode security metadata.
cat "$r/speaker-compat/start.sh" > "$m/etc/tb371fc-speaker/start.sh"
cmp "$r/speaker-compat/start.sh" "$m/etc/tb371fc-speaker/start.sh"
umount "$m"
e2fsck -fn "$r/integrated-network/system_ext-hwprofile.img" > "$r/speaker-compat/system_ext-hwprofile-fsck.log" 2>&1
