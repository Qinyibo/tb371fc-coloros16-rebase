#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
out="$r/erofs-runtime-vm"
test ! -e "$out"
mkdir -p "$out"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
aarch64-linux-gnu-gcc -static -O2 -Wall "$r/erofs_vm_init.c" -o "$out/init"
cp /work/tb371fc-erofs-minimal-vm-20261001/Image "$out/Image"
python3 "$r/build_vm_initramfs.py" "$r"
bash "$r/qemu_runtime.sh"
