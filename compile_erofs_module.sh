#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
out="$r/erofs-module-r107"
exec 9>>/work/tb371fc-wake-20261031/build.lock
flock -n 9
export PATH=/usr/lib/llvm-21/bin:$PATH LD_LIBRARY_PATH=/root/tc-shim/lib TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
make -C /work/tb371fc-wake-20261031/src O=/work/tb371fc-wake-20261031/out M="$out" -j4 ARCH=arm64 CC=clang CLANG_TRIPLE=aarch64-linux-gnu- CROSS_COMPILE=aarch64-linux-gnu- AS=aarch64-linux-gnu-as LOCALVERSION= KCFLAGS=-Wno-error modules > "$out/build.log" 2>&1
sha256sum -c "$out/kernel-preimages.sha256" > "$out/kernel-input-retention.log"
echo EROFS_R107_MODULE_BUILT
