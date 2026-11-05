#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
out="$r/erofs-runtime-vm"
timeout 100 qemu-system-aarch64 -M virt -cpu cortex-a57 -m 768 -smp 2 -nographic -no-reboot -nic none \
 -kernel "$out/Image" -initrd "$out/initramfs.cpio.gz" \
 -append 'console=ttyAMA0 rdinit=/init panic=-1' \
 -drive if=none,file="$r/apex-inputs/com.android.runtime/apex_payload.img",format=raw,readonly=on,id=original \
 -device virtio-blk-device,drive=original > "$out/serial.log" 2>&1
grep -E 'MOUNT |RESULT |FAIL |EROFS' "$out/serial.log" | tail -15

python3 - "$out" <<'PY'
import pathlib,re,sys,json
r=pathlib.Path(sys.argv[1]);s=(r/"serial.log").read_text(errors="replace");m=re.search(r"RESULT files=(\d+) dirs=(\d+) links=(\d+) bytes=(\d+) errors=(\d+)",s);assert m and tuple(map(int,m.groups()))==(21,8,15,12134185,0),s[-2000:]
(r/"result.json").write_text(json.dumps(dict(scope="Original runtime EROFS reads in retained VM only; actual separately built r107 module failed device file checks and is not qualified",files=21,links=15,bytes=12134185,errors=0),indent=2))
PY
