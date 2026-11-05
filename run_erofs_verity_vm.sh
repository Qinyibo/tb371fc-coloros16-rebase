#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
k="$r/erofs-kernel-vm"
out="$k/runtime-test"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
mkdir "$out"
python3 - "$r" "$out" <<'PY'
import pathlib,re,sys,hashlib
r,o=map(pathlib.Path,sys.argv[1:])
p=r/'apex-inputs/com.android.runtime'
s=(p/'avb-info.txt').read_text()
def find(pattern):
 x=re.findall(pattern,s,re.M);assert len(x)==1,x;return x[0]
data=int(find(r'^      Image Size:\s+(\d+) bytes'))
tree=int(find(r'^      Tree Offset:\s+(\d+)'))
assert data==tree and data%4096==0 and find(r'^      Data Block Size:\s+(\d+) bytes')=='4096' and find(r'^      Hash Block Size:\s+(\d+) bytes')=='4096'
assert find(r'^Public key \(sha1\):\s+(\w+)')==hashlib.sha1((p/'apex_pubkey').read_bytes()).hexdigest()
root=find(r'^      Root Digest:\s+(\w+)');salt=find(r'^      Salt:\s+(\w+)')
c=(r/'erofs_vm_init.c').read_text()
func=(r/'erofs_vm_verity.c.inc').read_text()
declarations=f'#define AVB_DATA_BYTES {data}u\n#define AVB_TREE_OFFSET {tree}u\n#define AVB_ROOT_DIGEST "{root}"\n#define AVB_SALT "{salt}"\n'
needle='int main(void) {'
assert c.count(needle)==1
c=c.replace(needle,declarations+func+'\n'+needle)
old=' int a=mount("/dev/vda","/erofs","erofs",MS_RDONLY,NULL),ea=errno;'
assert c.count(old)==1
c=c.replace(old,'''
 if(verity()){printf("FATAL verity setup\\n");reboot(RB_POWER_OFF);return 1;}
 int f=open("/dev/verity-apex",O_RDONLY);char block[4096];
 errno=0;ssize_t read0=pread(f,block,sizeof(block),0);int read_errno=errno;
 if(f>=0)close(f);
 printf("VERITY_PROBE bytes=%zd errno=%d\\n",read0,read_errno);
 if(read0<0){reboot(RB_POWER_OFF);return 1;}
 errno=0;
 int a=mount("/dev/verity-apex","/erofs","erofs",MS_RDONLY,NULL),ea=errno;''')
(o/'init.c').write_text(c)
z=bytearray((p/'apex_payload.img').read_bytes())
z[2048]^=1
(o/'corrupted-control.img').write_bytes(z)
PY
aarch64-linux-gnu-gcc -static -O2 -Wall "$out/init.c" -o "$out/init"
python3 "$r/build_vm_verity_initramfs.py" "$r" "$out" 2> "$out/initramfs.log"
for mode in official corrupted; do
 image="$r/apex-inputs/com.android.runtime/apex_payload.img"
 if test "$mode" = corrupted; then image="$out/corrupted-control.img"; fi
 timeout 70 qemu-system-aarch64 -M virt -cpu cortex-a57 -m 768 -smp 2 -nographic -no-reboot -nic none -kernel "$k/Image" -initrd "$out/initramfs.cpio.gz" -append 'console=ttyAMA0 rdinit=/init panic=-1' -drive if=none,file="$image",format=raw,readonly=on,id=runtime -device virtio-blk-device,drive=runtime > "$out/$mode.log" 2>&1
 grep -E 'DM_VERITY|VERITY_PROBE|RESULT|verity:|FATAL' "$out/$mode.log" | tail -8
done
grep -q 'VERITY_PROBE bytes=4096 errno=0' "$out/official.log"
grep -q 'RESULT files=21 dirs=8 links=15 bytes=12134185 errors=0' "$out/official.log"
grep -q 'VERITY_PROBE bytes=-1 errno=5' "$out/corrupted.log"
grep -q 'data block 0 is corrupted' "$out/corrupted.log"
echo BUILTIN_EROFS_AVB_VERITY_RUNTIME_POSITIVE_AND_NEGATIVE_PASS
