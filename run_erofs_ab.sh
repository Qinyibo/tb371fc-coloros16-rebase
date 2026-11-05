#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
export PATH=/usr/lib/llvm-21/bin:$PATH LD_LIBRARY_PATH=/root/tc-shim/lib TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
src=/root/tb371fc-c16-bpf-vm-src-20260930
ws=/work/tb371fc-erofs-minimal-vm-20261001
for mode in vm-control vm-partial; do
 out="$r/erofs-lz4-ab/$mode"
 sed -i 's/"erofs_pcluster-%u"/"erofs_ab_pcluster-%u"/g' "$out/zdata.c"
 (flock -n 9; make -C "$src" O="$ws/out" M="$out" -j4 ARCH=arm64 CC=clang CLANG_TRIPLE=aarch64-linux-gnu- CROSS_COMPILE=aarch64-linux-gnu- AS=aarch64-linux-gnu-as LOCALVERSION= KCFLAGS=-Wno-error modules) 9<"$ws/build.lock" > "$out/build.log" 2>&1
 aarch64-linux-gnu-gcc -static -O2 -Wall "$r/erofs_vm_ab_init.c" -o "$out/init"
 python3 "$r/build_vm_ab_initramfs.py" "$r" "$out"
 timeout 85 qemu-system-aarch64 -M virt -cpu cortex-a57 -m 768 -smp 2 -nographic -no-reboot -nic none -kernel "$r/erofs-runtime-vm/Image" -initrd "$out/initramfs.cpio.gz" -append 'console=ttyAMA0 rdinit=/init panic=-1' -drive if=none,file="$r/apex-inputs/com.android.runtime/apex_payload.img",format=raw,readonly=on,id=original -device virtio-blk-device,drive=original > "$out/serial.log" 2>&1
 grep -E 'MODULE |MOUNT |RESULT |FAIL |WARNING:|BUG:' "$out/serial.log" | tail -25
done
