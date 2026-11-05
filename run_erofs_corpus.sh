#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
out="$r/erofs-lz4-ab/corpus"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
aarch64-linux-gnu-gcc -static -O2 -Wall "$r/erofs_vm_corpus.c" -o "$r/erofs-lz4-ab/corpus-init"
python3 "$r/build_erofs_corpus.py" "$r"
for archive in "$out"/batch-*.cpio.gz; do
 log="${archive%.cpio.gz}.log"
 timeout 95 qemu-system-aarch64 -M virt -cpu cortex-a57 -m 1152 -smp 2 -nographic -no-reboot -nic none -kernel "$r/erofs-runtime-vm/Image" -initrd "$archive" -append 'console=ttyAMA0 rdinit=/init panic=-1' > "$log" 2>&1
 grep -E '^(APEX|BATCH|FAIL|FATAL) ' "$log"
done
