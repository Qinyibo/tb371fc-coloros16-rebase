import pathlib,re,shutil,sys
r=pathlib.Path(sys.argv[1]); old=r/'erofs-module-r107'; up=r/'erofs-upstream/source-5.15.224'
for mode in ('vm-control','vm-partial','r107-partial'):
 out=r/'erofs-lz4-ab'/mode; out.mkdir(parents=True)
 for f in old.iterdir():
  if f.suffix in ('.c','.h') and not f.name.endswith('.mod.c') or f.name=='Makefile': shutil.copyfile(f,out/f.name)
 shutil.copytree(old/'include',out/'include')
 p=out/'Makefile'; mk=p.read_text()
 if mode.startswith('vm'):
  p2=out/'super.c'; txt=p2.read_text()
  for x,y in [('"erofs",','"erofs_ab",'),('"erofs_inode"','"erofs_ab_inode"'),('"erofs_pcluster"','"erofs_ab_pcluster"')]: txt=txt.replace(x,y)
  p2.write_text(txt)
  p2=out/'erofs_compat.h'; p2.write_text('#include <linux/magic.h>\n#ifndef EROFS_SUPER_MAGIC_V1\n#define EROFS_SUPER_MAGIC_V1 0xE0F5E1E2\n#endif\n')
 if mode.endswith('partial'):
  # Keep upstream decoder core verbatim and restrict linkage to one EROFS caller.
  raw=(up/'lz4_decompress.c').read_text()
  body=raw[:raw.index('\nint LZ4_decompress_safe(')]
  head='int LZ4_decompress_safe_partial('
  start=raw.index(head); end=raw.index('\nint LZ4_decompress_fast(',start)
  body+=raw[start:end].replace(head,'int erofs_lz4_decompress_safe_partial(')
  (out/'lz4_partial.c').write_text(body)
  shutil.copyfile(up/'lz4defs.h',out/'lz4defs.h')
  p2=out/'decompressor.c'; txt=p2.read_text()
  decl='int erofs_lz4_decompress_safe_partial(const char *src, char *dst,\n\t\tint compressedSize, int targetOutputSize, int dstCapacity);\n'
  txt=txt.replace('#include <linux/lz4.h>','#include <linux/lz4.h>\n\n'+decl)
  assert txt.count('ret = LZ4_decompress_safe_partial(')==1
  p2.write_text(txt.replace('ret = LZ4_decompress_safe_partial(','ret = erofs_lz4_decompress_safe_partial('))
  mk=mk.replace('zmap.o zdata.o','zmap.o zdata.o lz4_partial.o')
 p.write_text(mk)
