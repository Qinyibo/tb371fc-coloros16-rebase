#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104/scheduler-compat
export TMPDIR="$r/tests/temp"
mkdir -p "$TMPDIR" "$r/tests/fs"
if ! test -f "$r/tests/fixture.ext4"; then
 truncate -s 16M "$r/tests/fixture.ext4"
 mkfs.ext4 -q -F "$r/tests/fixture.ext4"
fi
mount -t ext4 -o loop,rw "$r/tests/fixture.ext4" "$r/tests/fs"
trap 'umount "$r/tests/fs"' EXIT
mkdir -p "$r/tests/fs/cgroup/foreground" "$r/tests/fs/data"
chmod 700 "$r/tests/fs/data"
printf 0 > "$r/tests/fs/cgroup/foreground/schedtune.boost"
printf 0 > "$r/tests/fs/cgroup/foreground/schedtune.prefer_idle"
: > "$r/tests/fs/cgroup/tasks"
: > "$r/tests/fs/cgroup/foreground/tasks"
gcc -O2 -Wall -Wextra -Werror -Wno-misleading-indentation -Wno-format-truncation "$r/tests/lifecycle.c" -o "$r/tests/lifecycle"
"$r/tests/lifecycle" "$r/tests/fs" > "$r/tests/lifecycle.log" 2>&1
cat "$r/tests/lifecycle.log"
