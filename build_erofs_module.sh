#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
src=/root/tb371fc-c16-bpf-vm-src-20260930/fs/erofs
tree=/work/tb371fc-wake-20261031/src
kout=/work/tb371fc-wake-20261031/out
out="$r/erofs-module-r107"
test ! -e "$out"
mkdir -p "$out"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
exec 9>>/work/tb371fc-wake-20261031/build.lock
flock -n 9
sha256sum "$kout/.config" "$kout/Module.symvers" > "$out/kernel-preimages.sha256"
cp "$kout/Module.symvers" "$out/kernel-Module.symvers.input"
python3 - "$src" "$out" <<'PY'
import hashlib,json,pathlib,sys
src,out=map(pathlib.Path,sys.argv[1:]);rows=[]
for p in sorted(src.iterdir()):
 if p.suffix not in ('.c','.h'):continue
 raw=p.read_bytes();(out/p.name).write_bytes(raw);rows.append(dict(source=str(p),name=p.name,sha256=hashlib.sha256(raw).hexdigest()))
(out/'source-receipt.json').write_text(json.dumps(dict(scope='Existing locally retained and VM-tested EROFS source; only build wrappers added; no hardware driver/kernel Image replaced',files=rows),indent=2))
PY
cat > "$out/erofs_compat.h" <<'EOF'
/* Private module-only equivalents of the helpers used in the retained VM.
 * The production kernel headers and their exported ABI are not edited. */
#include <linux/pagemap.h>
#include <linux/magic.h>
#ifndef EROFS_SUPER_MAGIC_V1
#define EROFS_SUPER_MAGIC_V1 0xE0F5E1E2
#endif
static inline void attach_page_private(struct page *page, void *data)
{
 get_page(page);
 set_page_private(page, (unsigned long)data);
 SetPagePrivate(page);
}
static inline void *detach_page_private(struct page *page)
{
 void *data = (void *)page_private(page);
 if (!PagePrivate(page)) return NULL;
 ClearPagePrivate(page);
 set_page_private(page, 0);
 put_page(page);
 return data;
}
EOF
cat > "$out/Makefile" <<'EOF'
obj-m := erofs.o
erofs-y := super.o inode.o data.o namei.o dir.o utils.o pcpubuf.o xattr.o decompressor.o zmap.o zdata.o
ccflags-y += -DCONFIG_EROFS_FS_XATTR -DCONFIG_EROFS_FS_ZIP -DCONFIG_EROFS_FS_SECURITY -DCONFIG_EROFS_FS_POSIX_ACL
ccflags-y += -include $(src)/erofs_compat.h
ccflags-y += -I$(src)/include
EOF
mkdir -p "$out/include/trace/events"
cp /root/tb371fc-c16-bpf-vm-src-20260930/include/trace/events/erofs.h "$out/include/trace/events/erofs.h"
export PATH=/usr/lib/llvm-21/bin:$PATH LD_LIBRARY_PATH=/root/tc-shim/lib
make -C "$tree" O="$kout" M="$out" -j4 ARCH=arm64 CC=clang CLANG_TRIPLE=aarch64-linux-gnu- CROSS_COMPILE=aarch64-linux-gnu- AS=aarch64-linux-gnu-as LOCALVERSION= KCFLAGS=-Wno-error modules > "$out/build.log" 2>&1
sha256sum -c "$out/kernel-preimages.sha256" > "$out/kernel-input-retention.log"
test -f "$out/erofs.ko"
echo EROFS_R107_MODULE_BUILT
