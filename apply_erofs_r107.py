import pathlib,shutil,sys
r=pathlib.Path(sys.argv[1]); src=pathlib.Path(sys.argv[2]); old=r/'erofs-lz4-ab/r107-partial'
def edit(p,orig,change):
 s=p.read_text()
 assert s.count(orig)==1,(p,orig,s.count(orig))
 p.write_text(s.replace(orig,change))
port=src/'fs/erofs'; port.mkdir()
for p in old.iterdir():
 if p.suffix in ('.c','.h') and not p.name.endswith('.mod.c'):
  shutil.copyfile(p,port/p.name)
shutil.copyfile(old/'include/trace/events/erofs.h',src/'include/trace/events/erofs.h')
vm=pathlib.Path('/root/tb371fc-c16-bpf-vm-src-20260930/fs/erofs')
for p in ('Kconfig','Makefile'): shutil.copyfile(vm/p,port/p)
edit(port/'Makefile','decompressor.o zmap.o zdata.o','decompressor.o zmap.o zdata.o lz4_partial.o')
edit(port/'internal.h','#define EROFS_SUPER_MAGIC   EROFS_SUPER_MAGIC_V1','#include "erofs_compat.h"\n#define EROFS_SUPER_MAGIC   EROFS_SUPER_MAGIC_V1')
p=port/'erofs_compat.h'
s=p.read_text()
s=s.replace('/* Private module-only equivalents of the helpers used in the retained VM.\n * The production kernel headers and their exported ABI are not edited. */','''/* SPDX-License-Identifier: GPL-2.0-only */
#ifndef __EROFS_COMPAT_H
#define __EROFS_COMPAT_H
/* Private 4.19 equivalents of the newer pagemap helpers. */''').replace('static inline void attach_page_private','static inline void erofs_attach_page_private').replace('static inline void *detach_page_private','static inline void *erofs_detach_page_private')
p.write_text(s+'\n#endif /* __EROFS_COMPAT_H */\n')
p=port/'zdata.c';s=p.read_text();p.write_text(s.replace('attach_page_private(', 'erofs_attach_page_private(').replace('detach_page_private(', 'erofs_detach_page_private('))
# The stable 5.15 backport of 21e161de2dc6 uses this same guard.
edit(port/'decompressor.c','if (rq->partial_decoding || !support_0padding ||\n\t\t    ofull - oend','if (rq->partial_decoding || !support_0padding ||\n\t\t    nrpages_out < nrpages_in ||\n\t\t    ofull - oend')
edit(src/'fs/Kconfig','source "fs/squashfs/Kconfig"','source "fs/squashfs/Kconfig"\nsource "fs/erofs/Kconfig"')
edit(src/'fs/Makefile','obj-$(CONFIG_SQUASHFS)\t\t+= squashfs/','obj-$(CONFIG_SQUASHFS)\t\t+= squashfs/\nobj-$(CONFIG_EROFS_FS)\t\t+= erofs/')
edit(src/'drivers/staging/Kconfig','source "drivers/staging/erofs/Kconfig"\n','')
edit(src/'drivers/staging/Makefile','obj-$(CONFIG_EROFS_FS)\t\t+= erofs/\n','')
