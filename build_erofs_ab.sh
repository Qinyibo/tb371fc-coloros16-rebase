#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
export PATH=/usr/lib/llvm-21/bin:$PATH LD_LIBRARY_PATH=/root/tc-shim/lib TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
python3 "$r/prepare_erofs_ab.py" "$r"
for mode in vm-control vm-partial r107-partial; do
  out="$r/erofs-lz4-ab/$mode"
  if [[ "$mode" = r107-* ]]; then
    ws=/work/tb371fc-wake-20261031
    src="$ws/src"
  else
    ws=/work/tb371fc-erofs-minimal-vm-20261001
    src=/root/tb371fc-c16-bpf-vm-src-20260930
  fi
  ( flock -n 9; make -C "$src" O="$ws/out" M="$out" -j4 ARCH=arm64 CC=clang CLANG_TRIPLE=aarch64-linux-gnu- CROSS_COMPILE=aarch64-linux-gnu- AS=aarch64-linux-gnu-as LOCALVERSION= KCFLAGS=-Wno-error modules ) 9<"$ws/build.lock" > "$out/build.log" 2>&1 || { tail -35 "$out/build.log"; exit 1; }
  sha256sum "$out/erofs.ko"
done
sha256sum -c "$r/erofs-module-r107/kernel-preimages.sha256"
