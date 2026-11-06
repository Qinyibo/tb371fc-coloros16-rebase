Instruction range [0x709a4, 0x70c1c); symbol names omitted for stripped local functions.
000709a4: lsl     x8, x22, #0x12
000709a8: adrp    x9, #0xaf000
000709ac: str     x8, [x9, #0x10]
000709b0: adrp    x8, #0xae000
000709b4: ldr     x0, [x8, #0xff8]
000709b8: ldr     x8, [x0]
000709bc: ldr     x8, [x8]
000709c0: blr     x8
000709c4: adrp    x8, #0xae000
000709c8: mov     w23, w0
000709cc: ldr     x0, [x8, #0xff8]
000709d0: adrp    x9, #0xaf000
000709d4: ldr     x21, [x9]
000709d8: ldr     x8, [x0]
000709dc: ldr     x8, [x8, #0x10]
000709e0: blr     x8
000709e4: mov     x22, x0
000709e8: tbz     w23, #0, #0x70a8c
000709ec: bl      #0x71494
000709f0: tbz     w0, #0, #0x70a48
000709f4: str     xzr, [sp, #0x60]
000709f8: str     xzr, [sp, #0x48]
000709fc: stp     xzr, xzr, [x29, #-0x70]
00070a00: add     x0, sp, #0x60
00070a04: add     x1, sp, #0x48
00070a08: sub     x2, x29, #0x68
00070a0c: sub     x3, x29, #0x70
00070a10: mov     w4, #1
00070a14: bl      #0x6f860
00070a18: tbz     w0, #0, #0x70cdc
00070a1c: ldr     x0, [sp, #0x60]
00070a20: ldr     x8, [sp, #0x48]
00070a24: sub     x1, x8, x0
00070a28: bl      #0x72684
00070a2c: tbnz    w0, #0, #0x70a48
00070a30: adrp    x1, #0x88000
00070a34: adrp    x2, #0x88000
00070a38: add     x1, x1, #0x8e8 ; 0x888e8 'expand_helper'
00070a3c: add     x2, x2, #0xc12 ; 0x88c12 '[-]remap_next_map init fail'
00070a40: mov     w0, #5
00070a44: bl      #0x11cc0 ; PLT reloc __android_log_print
00070a48: adrp    x8, #0xaf000
00070a4c: ldr     x23, [x8, #0x38]
00070a50: bl      #0x6d930
00070a54: mov     x1, x0
00070a58: add     x0, sp, #0x48
00070a5c: bl      #0x14a80
00070a60: adrp    x8, #0xaf000
00070a64: ldr     x2, [x8, #0x10]
00070a68: ldr     x1, [sp, #0x30]
00070a6c: add     x8, sp, #0x60
00070a70: add     x0, sp, #0x48
00070a74: blr     x23
00070a78: add     x21, x22, x21
00070a7c: ldrb    w8, [x21]
00070a80: tbnz    w8, #0, #0x70b50
00070a84: strh    wzr, [x21]
00070a88: b       #0x70b70
00070a8c: adrp    x8, #0xaf000
00070a90: ldr     x19, [x8, #0x40]
00070a94: bl      #0x6d930
00070a98: mov     x1, x0
00070a9c: add     x0, sp, #0x60
00070aa0: bl      #0x14a80
00070aa4: adrp    x8, #0xaf000
00070aa8: ldr     x2, [x8, #0x10]
00070aac: ldr     x1, [sp, #0x30]
00070ab0: add     x0, sp, #0x60
00070ab4: blr     x19
00070ab8: ldrb    w8, [sp, #0x60]
00070abc: mov     x23, x0
00070ac0: tbz     w8, #0, #0x70acc
00070ac4: ldr     x0, [sp, #0x70]
00070ac8: bl      #0x11780 ; PLT reloc _ZdlPv
00070acc: str     x23, [x21, x22]
00070ad0: adrp    x1, #0x88000
00070ad4: adrp    x2, #0x88000
00070ad8: add     x1, x1, #0x8e8 ; 0x888e8 'expand_helper'
00070adc: add     x2, x2, #0xc5c ; 0x88c5c '[+]legacy live bitmap expand on:%p'
00070ae0: mov     w0, #3
00070ae4: mov     x3, x23
00070ae8: bl      #0x11cc0 ; PLT reloc __android_log_print
00070aec: add     x0, sp, #0x60
00070af0: add     x1, sp, #0x48
00070af4: sub     x2, x29, #0x68
00070af8: sub     x3, x29, #0x70
00070afc: mov     w4, #1
00070b00: bl      #0x6f860
00070b04: tbz     w0, #0, #0x70b34
00070b08: ldr     x0, [sp, #0x60]
00070b0c: ldr     x1, [sp, #0x48]
00070b10: bl      #0x6ea74
00070b14: tbz     w0, #0, #0x70cf8
00070b18: adrp    x1, #0x88000
00070b1c: adrp    x2, #0x88000
00070b20: add     x1, x1, #0x8e8 ; 0x888e8 'expand_helper'
00070b24: add     x2, x2, #0xc7f ; 0x88c7f '[+]unmap origin bitmap done'
00070b28: mov     w0, #3
00070b2c: bl      #0x11cc0 ; PLT reloc __android_log_print
00070b30: b       #0x70d2c
00070b34: adrp    x1, #0x88000
00070b38: adrp    x2, #0x89000
00070b3c: add     x1, x1, #0x8e8 ; 0x888e8 'expand_helper'
00070b40: add     x2, x2, #0x695 ; 0x89695 'parse_live_bitmaps() fail'
00070b44: mov     w0, #5
00070b48: bl      #0x11cc0 ; PLT reloc __android_log_print
00070b4c: b       #0x70d2c
00070b50: ldr     x8, [x21, #0x10]
00070b54: strb    wzr, [x8]
00070b58: ldrb    w8, [x21]
00070b5c: str     xzr, [x21, #8]
00070b60: tbz     w8, #0, #0x70b70
00070b64: ldr     x0, [x21, #0x10]
00070b68: bl      #0x11780 ; PLT reloc _ZdlPv
00070b6c: str     xzr, [x21]
00070b70: ldr     x8, [sp, #0x70]
00070b74: ldr     q0, [sp, #0x60]
00070b78: mov     x22, x21
00070b7c: add     x9, sp, #0x60
00070b80: str     x8, [x21, #0x10]
00070b84: str     q0, [x21]
00070b88: stp     xzr, xzr, [sp, #0x68]
00070b8c: str     xzr, [sp, #0x60]
00070b90: ldur    q0, [sp, #0x98]
00070b94: ldur    q1, [sp, #0x78]
00070b98: ldur    q2, [sp, #0x88]
00070b9c: ldrb    w8, [x22, #0x68]!
00070ba0: add     x23, x9, #0x68
00070ba4: stp     q1, q2, [x22, #-0x50]
00070ba8: stur    q0, [x22, #-0x30]
00070bac: ldur    q0, [sp, #0xa8]
00070bb0: ldur    q1, [sp, #0xb8]
00070bb4: stp     q0, q1, [x22, #-0x20]
00070bb8: tbnz    w8, #0, #0x70bc4
00070bbc: strh    wzr, [x22]
00070bc0: b       #0x70be4
00070bc4: ldr     x8, [x21, #0x78]
00070bc8: strb    wzr, [x8]
00070bcc: ldrb    w8, [x21, #0x68]
00070bd0: str     xzr, [x21, #0x70]
00070bd4: tbz     w8, #0, #0x70be4
00070bd8: ldr     x0, [x21, #0x78]
00070bdc: bl      #0x11780 ; PLT reloc _ZdlPv
00070be0: str     xzr, [x21, #0x68]
00070be4: ldr     x8, [x23, #0x10]
00070be8: ldr     q0, [x23]
00070bec: str     x8, [x22, #0x10]
00070bf0: str     q0, [x22]
00070bf4: stp     xzr, xzr, [x23, #8]
00070bf8: str     xzr, [x23]
00070bfc: ldrb    w8, [sp, #0x60]
00070c00: tbz     w8, #0, #0x70c0c
00070c04: ldr     x0, [sp, #0x70]
00070c08: bl      #0x11780 ; PLT reloc _ZdlPv
00070c0c: ldrb    w8, [sp, #0x48]
00070c10: tbz     w8, #0, #0x70c1c
00070c14: ldr     x0, [sp, #0x58]
00070c18: bl      #0x11780 ; PLT reloc _ZdlPv
