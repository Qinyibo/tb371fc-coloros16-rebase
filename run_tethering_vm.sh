#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
p="$r/bpf-compat"
a="$p/rebuilt-tethering"
o="$p/tethering-vm"
w=/work/tb371fc-c16-bpf-vm-v3-20261001
k="$r/erofs-kernel-vm"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
mkdir "$o"
work=$(mktemp -d /work/tb371fc-network-vm.XXXXXXXX)
mkdir "$work/ref" "$work/src" "$work/daily" "$work/rebuilt"
trap 'for m in "$work/src" "$work/daily" "$work/rebuilt"; do if mountpoint -q "$m"; then umount "$m"; fi; done' EXIT
mount -t erofs -o ro,loop "$p/donor-apex_payload.img" "$work/src"
mount -t ext4 -o ro,noload,loop "$p/daily-apex_payload.img" "$work/daily"
mount -t erofs -o ro,loop "$a/apex_payload.img" "$work/rebuilt"
rsync -aHAX --numeric-ids "$work/src/" "$work/ref/"
python3 - "$r" "$w" "$o" "$work" <<'PY'
import hashlib,json,pathlib,re,sys
r,w,o,work=map(pathlib.Path,sys.argv[1:]); p=r/'bpf-compat'; a=p/'rebuilt-tethering'
patches=json.loads((a/'patches.json').read_text()); sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,(before,after,_) in patches.items():
 assert sha(work/'ref'/n)==before
 data=(work/'daily'/n).read_bytes(); assert hashlib.sha256(data).hexdigest()==after
 (work/'ref'/n).write_bytes(data)
objs=json.loads((w/'probe-inputs.json').read_text())['objects']
assert len(objs)==5
for b in objs:
 assert sha(work/'ref/etc/bpf'/b['file'])==sha(w/'candidate-bpf'/b['file'])==b['sha256']
(o/'bpf-inputs.json').write_text(json.dumps(objs,indent=2)+'\n')
s=(a/'payload-info.txt').read_text()
def find(pattern):
 x=re.findall(pattern,s,re.M);assert len(x)==1,x;return x[0]
data=int(find(r'^      Image Size:\s+(\d+) bytes')); tree=int(find(r'^      Tree Offset:\s+(\d+)'))
assert data==tree and data%4096==0 and find(r'^      Data Block Size:\s+(\d+) bytes')=='4096' and find(r'^      Hash Block Size:\s+(\d+) bytes')=='4096'
assert find(r'^Public key \(sha1\):\s+(\w+)')==hashlib.sha1((a/'apex_pubkey').read_bytes()).hexdigest()
root=find(r'^      Root Digest:\s+(\w+)'); salt=find(r'^      Salt:\s+(\w+)')
c=(r/'erofs_vm_init.c').read_text(); func=(r/'erofs_vm_verity.c.inc').read_text()
probe=(w/'probe.c').read_text()
assert probe.count('int main(void) {')==1
probe=probe.replace('int main(void) {','static int run_network_probe(void) {')
probe=probe.replace('  sync(); reboot(RB_POWER_OFF); for(;;)pause();','  return mfail || pfail || extra_fail || lf || rf;')
assert 'return mfail || pfail || extra_fail || lf || rf;' in probe
(o/'network-probe.inc').write_text(probe)
declarations=f'#define AVB_DATA_BYTES {data}u\n#define AVB_TREE_OFFSET {tree}u\n#define AVB_ROOT_DIGEST "{root}"\n#define AVB_SALT "{salt}"\n'
c=c.replace('int main(void) {',declarations+func+'\n#include "network-probe.inc"\nint main(void) {')
c=c.replace(' int a=mount("/dev/vda","/erofs","erofs",MS_RDONLY,NULL),ea=errno;', '''
 if(verity()){printf("FATAL verity setup\\n");reboot(RB_POWER_OFF);return 1;}
 int a=mount("/dev/verity-apex","/erofs","erofs",MS_RDONLY,NULL),ea=errno;''')
files=sum(p.is_file() and not p.is_symlink() for p in (work/'ref').rglob('*'))
dirs=1+sum(p.is_dir() and not p.is_symlink() for p in (work/'ref').rglob('*'))
links=sum(p.is_symlink() for p in (work/'ref').rglob('*'))
size=sum(p.stat().st_size for p in (work/'ref').rglob('*') if p.is_file() and not p.is_symlink())
assert files+dirs+links==74
c=c.replace('files!=21||dirs!=8||links!=15||bytes!=12134185ULL',f'files!={files}||dirs!={dirs}||links!={links}||bytes!={size}ULL')
c=c.replace(' sync();reboot(RB_POWER_OFF);return errors?1:0;', ' if(!errors) errors=run_network_probe();\n printf("TETHERING_VM_RESULT errors=%d\\n",errors);\n sync();reboot(RB_POWER_OFF);return errors?1:0;')
(o/'init.c').write_text(c)
base=(r/'build_vm_verity_initramfs.py').read_text().replace("root=r/'mounts/com.android.runtime'",f"root=pathlib.Path({str(work/'ref')!r})")
(o/'make_initramfs.py').write_text(base)
PY
python3 "$r/verify_apex_tree.py" "$work/ref" "$work/rebuilt" "$o" verify
# EROFS and policy inputs are read from the signed payload before loading the verified BPF instructions.
aarch64-linux-gnu-gcc -static -O2 "$o/init.c" -o "$o/init"
python3 "$o/make_initramfs.py" "$r" "$o"
sha256sum "$k/Image" "$a/apex_payload.img" "$o/initramfs.cpio.gz" > "$o/inputs.SHA256SUMS"
timeout 110 qemu-system-aarch64 -M virt -cpu cortex-a57 -m 768 -smp 2 -nographic -no-reboot -nic none -kernel "$k/Image" -initrd "$o/initramfs.cpio.gz" -append 'console=ttyAMA0 rdinit=/init panic=-1 c16_realuid_vm=1' -drive if=none,file="$a/apex_payload.img",format=raw,readonly=on,id=tether -device virtio-blk-device,drive=tether > "$o/serial.log" 2>&1
for result in 'DM_VERITY_READY' 'RESULT files=.*errors=0' 'PROBE_COMPLETE maps_failed=0 mandatory_programs_failed=0 candidate_programs_failed=0' 'LOCALNET_COMPLETE cases=24 failed=0' 'REALUID_COMPLETE cases=10 failed=0' 'TETHERING_VM_RESULT errors=0'; do grep -E "$result" "$o/serial.log"; done
