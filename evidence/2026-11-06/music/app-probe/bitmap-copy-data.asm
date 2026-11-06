Instruction range [0x70c44, 0x70cb0); symbol names omitted for stripped local functions.
00070c44: adrp    x1, #0x88000
00070c48: adrp    x2, #0x88000
00070c4c: add     x1, x1, #0x8e8 ; 0x888e8 'expand_helper'
00070c50: add     x2, x2, #0xdb1 ; 0x88db1 'copy_live_bitmap_fast()'
00070c54: mov     w0, #3
00070c58: bl      #0x11cc0 ; PLT reloc __android_log_print
00070c5c: add     x0, sp, #0x60
00070c60: add     x1, sp, #0x48
00070c64: sub     x2, x29, #0x68
00070c68: sub     x3, x29, #0x70
00070c6c: mov     w4, wzr
00070c70: bl      #0x6f860
00070c74: tbz     w0, #0, #0x70d14
00070c78: ldr     x3, [sp, #0x60]
00070c7c: ldr     x4, [sp, #0x48]
00070c80: ldp     x6, x5, [x29, #-0x70]
00070c84: adrp    x1, #0x88000
00070c88: adrp    x2, #0x88000
00070c8c: add     x1, x1, #0x8e8 ; 0x888e8 'expand_helper'
00070c90: add     x2, x2, #0xdc9 ; 0x88dc9 'memcpy [%p,%p] -> [%p,%p]'
00070c94: mov     w0, #4
00070c98: bl      #0x11cc0 ; PLT reloc __android_log_print
00070c9c: ldr     x1, [sp, #0x60]
00070ca0: ldr     x8, [sp, #0x48]
00070ca4: ldur    x0, [x29, #-0x68]
00070ca8: sub     x2, x8, x1
00070cac: bl      #0x11680 ; PLT reloc memcpy
