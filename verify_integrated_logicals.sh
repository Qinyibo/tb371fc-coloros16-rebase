#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
out="$r/integrated-logicals"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
for n in system system_ext product; do
 m="$out/verify-$n"; mkdir -p "$m"; mount -t ext4 -o ro,loop "$out/$n.img" "$m"
 if test "$n" != product; then
  m="$out/baseline-$n"; mkdir -p "$m"; mount -t ext4 -o ro,loop "$r/base-ext4-UNADAPTED/$n.img" "$m"
 fi
done
python3 "$r/verify_integrated_logicals.py" "$r"
