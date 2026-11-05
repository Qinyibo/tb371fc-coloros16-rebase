#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
policy="${1:-$r/integrated-logicals/runtime-sepolicy}"
out="$r/scheduler-compat/policy/candidate/vm"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
mkdir -p "$out"
aarch64-linux-gnu-gcc -static -O2 -Wall "$r/selinux_policy_vm.c" -o "$out/init"
python3 - "$r" "$out" "$policy" <<'PY'
import gzip,pathlib,sys
r,o,policy=map(pathlib.Path,sys.argv[1:])
b=bytearray()
for i,(name,mode,data,major,minor) in enumerate((
 ('dev',0o40755,b'',0,0),('dev/console',0o20600,b'',5,1),('selinux',0o40755,b'',0,0),
 ('init',0o100755,(o/'init').read_bytes(),0,0),('policy',0o100644,policy.read_bytes(),0,0),
 ('TRAILER!!!',0,b'',0,0)),1):
 n=name.encode()+b'\0';v=[i,mode,0,0,1,0,len(data),0,0,major,minor,len(n),0]
 b.extend(b'070701'+''.join(f'{x:08x}' for x in v).encode()+n);b.extend(b'\0'*(-len(b)%4))
 b.extend(data);b.extend(b'\0'*(-len(b)%4))
(o/'initramfs.cpio.gz').write_bytes(gzip.compress(b,mtime=0))
PY
ret=0
timeout 45 qemu-system-aarch64 -M virt -cpu cortex-a57 -m 768 -smp 2 -nographic -no-reboot -nic none -kernel "$r/erofs-kernel-vm/Image" -initrd "$out/initramfs.cpio.gz" -append 'console=ttyAMA0 rdinit=/init panic=-1 security=selinux enforcing=1' > "$out/serial.log" 2>&1 || ret=$?
test "$ret" -eq 0 || test "$ret" -eq 124
grep -E 'POLICY_|SELinux:|type=1403|permissive=0' "$out/serial.log" | tail -25
python3 - "$out" "$policy" <<'PY'
import hashlib,json,pathlib,re,sys
out,policy=map(pathlib.Path,sys.argv[1:])
s=(out/'serial.log').read_text()
a=re.search(r'POLICY_PRE version=(\d+) enforcing=1 bytes=(\d+)',s)
assert a and int(a.group(1))>=30 and int(a.group(2))==policy.stat().st_size
assert re.search(r'audit: type=1403 .*lsm=selinux res=1',s),s[-1200:]
assert re.search(r'audit: type=1400 .*avc:\s+denied.*permissive=0',s),s[-1200:]
(out/'result.json').write_text(json.dumps(dict(scope='ARM64 QEMU kernel accepted the assembled policy with enforcement enabled; no physical Android init or HAL claim',policy_max=int(a.group(1)),sha256=hashlib.sha256(policy.read_bytes()).hexdigest(),policy_load_audit_success=True,subsequent_enforcing_audit=True),indent=2)+'\n')
print('ASSEMBLED_SEPOLICY_LOADED_WITH_ENFORCING_ENABLED_IN_VM')
PY
