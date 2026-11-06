Instruction range [0x719cc, 0x71e4c); symbol names omitted for stripped local functions.
000719cc: sub     sp, sp, #0xc0
000719d0: stp     x28, x27, [sp, #0x60]
000719d4: stp     x26, x25, [sp, #0x70]
000719d8: stp     x24, x23, [sp, #0x80]
000719dc: stp     x22, x21, [sp, #0x90]
000719e0: stp     x20, x19, [sp, #0xa0]
000719e4: stp     x29, x30, [sp, #0xb0]
000719e8: add     x29, sp, #0xb0
000719ec: mrs     x28, tpidr_el0
000719f0: ldr     x8, [x28, #0x28]
000719f4: adrp    x0, #0x89000
000719f8: add     x0, x0, #0x1a7 ; 0x891a7 '_ZN3art2gc5space11RegionSpace5ClearEv'
000719fc: str     x8, [sp, #0x58]
00071a00: bl      #0x71064
00071a04: cbz     x0, #0x71da4
00071a08: mov     x20, x0
00071a0c: mov     x19, xzr
00071a10: movi    v0.2d, #0000000000000000
00071a14: mov     w26, #1
00071a18: cmn     x0, #0x12d
00071a1c: str     wzr, [sp, #0x50]
00071a20: str     xzr, [sp, #0x48]
00071a24: stp     q0, q0, [sp, #0x20]
00071a28: strb    w26, [sp, #0x20]
00071a2c: b.hi    #0x71de4
00071a30: mov     w24, #0x3c0
00071a34: adrp    x19, #0xa8000
00071a38: adrp    x21, #0xa8000
00071a3c: add     x25, x20, #0x12c
00071a40: movk    w24, #0xd65f, lsl #16
00071a44: add     x22, sp, #0x20
00071a48: add     x19, x19, #0x2d0 ; 0xa82d0 reloc 0xa7218
00071a4c: add     x21, x21, #0x2d8 ; 0xa82d8 reloc 0xa72c8
00071a50: mov     x23, x20
00071a54: b       #0x71a64
00071a58: add     x23, x23, #4
00071a5c: cmp     x23, x25
00071a60: b.hs    #0x71de0
00071a64: ldr     w27, [x23]
00071a68: cmp     w27, w24
00071a6c: b.eq    #0x71dc0
00071a70: add     x1, sp, #0x1c
00071a74: add     x2, sp, #0x18
00071a78: mov     w0, w27
00071a7c: bl      #0x6c258
00071a80: tbz     w0, #0, #0x71a9c
00071a84: ldrb    w8, [sp, #0x18]
00071a88: ldrb    w8, [x22, x8]
00071a8c: cbz     w8, #0x71a58
00071a90: ldrb    w8, [sp, #0x1c]
00071a94: strb    w26, [x22, x8]
00071a98: b       #0x71a58
00071a9c: add     x1, sp, #0x14
00071aa0: add     x2, sp, #0x10
00071aa4: add     x3, sp, #0xc
00071aa8: mov     w0, w27
00071aac: bl      #0x6c1f8
00071ab0: tbz     w0, #0, #0x71b08
00071ab4: ldrb    w8, [sp, #0x10]
00071ab8: ldrb    w8, [x22, x8]
00071abc: cbz     w8, #0x71a58
00071ac0: ldr     w3, [sp, #0x14]
00071ac4: adrp    x1, #0x89000
00071ac8: adrp    x2, #0x89000
00071acc: mov     w0, #3
00071ad0: add     x1, x1, #0x207 ; 0x89207 'offset_probe'
00071ad4: add     x2, x2, #0x183 ; 0x89183 'ldr imm12=%p'
00071ad8: bl      #0x11cc0 ; PLT reloc __android_log_print
00071adc: ldr     x8, [x19] ; load 0xa82d0 reloc 0xa7218
00071ae0: ldrsw   x27, [sp, #0x14]
00071ae4: mov     x0, x19
00071ae8: ldr     x8, [x8, #0x18]
00071aec: blr     x8
00071af0: cmp     x0, x27
00071af4: b.ne    #0x71b68
00071af8: strb    w26, [sp, #0x48]
00071afc: ldrb    w8, [sp, #0x49]
00071b00: cbnz    w8, #0x71b98
00071b04: b       #0x71ba8
00071b08: add     x1, sp, #0x14
00071b0c: add     x2, sp, #0x10
00071b10: add     x3, sp, #0xc
00071b14: mov     w0, w27
00071b18: bl      #0x6c1b0
00071b1c: tbz     w0, #0, #0x71a58
00071b20: ldr     w3, [sp, #0x14]
00071b24: adrp    x1, #0x89000
00071b28: adrp    x2, #0x89000
00071b2c: mov     w0, #3
00071b30: add     x1, x1, #0x207 ; 0x89207 'offset_probe'
00071b34: add     x2, x2, #0x1fa ; 0x891fa 'str imm12=%p'
00071b38: bl      #0x11cc0 ; PLT reloc __android_log_print
00071b3c: ldr     x8, [x19] ; load 0xa82d0 reloc 0xa7218
00071b40: ldrsw   x27, [sp, #0x14]
00071b44: mov     x0, x19
00071b48: ldr     x8, [x8, #0x48]
00071b4c: blr     x8
00071b50: cmp     x0, x27
00071b54: b.ne    #0x71c6c
00071b58: strb    w26, [sp, #0x4a]
00071b5c: ldrb    w8, [sp, #0x48]
00071b60: cbnz    w8, #0x71c94
00071b64: b       #0x71cac
00071b68: ldr     x8, [x19] ; load 0xa82d0 reloc 0xa7218
00071b6c: ldrsw   x27, [sp, #0x14]
00071b70: mov     x0, x19
00071b74: ldr     x8, [x8, #0x20]
00071b78: blr     x8
00071b7c: cmp     x0, x27
00071b80: b.ne    #0x71b88
00071b84: strb    w26, [sp, #0x49]
00071b88: ldrb    w8, [sp, #0x48]
00071b8c: cbz     w8, #0x71ba8
00071b90: ldrb    w8, [sp, #0x49]
00071b94: cbz     w8, #0x71ba8
00071b98: ldrb    w8, [sp, #0x4a]
00071b9c: cbz     w8, #0x71ba8
00071ba0: ldrb    w8, [sp, #0x4b]
00071ba4: cbnz    w8, #0x71e28
00071ba8: ldr     x8, [x21] ; load 0xa82d8 reloc 0xa72c8
00071bac: ldrsw   x27, [sp, #0x14]
00071bb0: mov     x0, x21
00071bb4: ldr     x8, [x8, #0x18]
00071bb8: blr     x8
00071bbc: cmp     x0, x27
00071bc0: b.ne    #0x71bdc
00071bc4: adrp    x21, #0xa8000
00071bc8: add     x21, x21, #0x2e0 ; 0xa82e0 reloc 0xa7378
00071bcc: strb    w26, [sp, #0x4c]
00071bd0: ldrb    w8, [sp, #0x4c]
00071bd4: cbnz    w8, #0x71c0c
00071bd8: b       #0x71c24
00071bdc: ldr     x8, [x21] ; load 0xa82e0 reloc 0xa7378
00071be0: ldrsw   x27, [sp, #0x14]
00071be4: mov     x0, x21
00071be8: ldr     x8, [x8, #0x20]
00071bec: blr     x8
00071bf0: adrp    x21, #0xa8000
00071bf4: cmp     x0, x27
00071bf8: add     x21, x21, #0x2e0 ; 0xa82e0 reloc 0xa7378
00071bfc: b.ne    #0x71c04
00071c00: strb    w26, [sp, #0x4d]
00071c04: ldrb    w8, [sp, #0x4c]
00071c08: cbz     w8, #0x71c24
00071c0c: ldrb    w8, [sp, #0x4d]
00071c10: cbz     w8, #0x71c24
00071c14: ldrb    w8, [sp, #0x4e]
00071c18: cbz     w8, #0x71c24
00071c1c: ldrb    w8, [sp, #0x4f]
00071c20: cbnz    w8, #0x71e18
00071c24: ldr     x8, [x21] ; load 0xa82e0 reloc 0xa7378
00071c28: ldrsw   x27, [sp, #0x14]
00071c2c: mov     x0, x21
00071c30: ldr     x8, [x8, #0x18]
00071c34: blr     x8
00071c38: cmp     x0, x27
00071c3c: b.ne    #0x71c48
00071c40: strb    w26, [sp, #0x50]
00071c44: b       #0x71d6c
00071c48: ldr     x8, [x21] ; load 0xa82e0 reloc 0xa7378
00071c4c: ldrsw   x27, [sp, #0x14]
00071c50: mov     x0, x21
00071c54: ldr     x8, [x8, #0x20]
00071c58: blr     x8
00071c5c: cmp     x0, x27
00071c60: b.ne    #0x71d6c
00071c64: strb    w26, [sp, #0x51]
00071c68: b       #0x71d6c
00071c6c: ldr     x8, [x19] ; load 0xa82d0 reloc 0xa7218
00071c70: ldrsw   x27, [sp, #0x14]
00071c74: mov     x0, x19
00071c78: ldr     x8, [x8, #0x50]
00071c7c: blr     x8
00071c80: cmp     x0, x27
00071c84: b.ne    #0x71c8c
00071c88: strb    w26, [sp, #0x4b]
00071c8c: ldrb    w8, [sp, #0x48]
00071c90: cbz     w8, #0x71cac
00071c94: ldrb    w8, [sp, #0x49]
00071c98: cbz     w8, #0x71cac
00071c9c: ldrb    w8, [sp, #0x4a]
00071ca0: cbz     w8, #0x71cac
00071ca4: ldrb    w8, [sp, #0x4b]
00071ca8: cbnz    w8, #0x71e28
00071cac: ldr     x8, [x21] ; load 0xa82e0 reloc 0xa7378
00071cb0: ldrsw   x27, [sp, #0x14]
00071cb4: mov     x0, x21
00071cb8: ldr     x8, [x8, #0x48]
00071cbc: blr     x8
00071cc0: cmp     x0, x27
00071cc4: b.ne    #0x71ce0
00071cc8: adrp    x21, #0xa8000
00071ccc: strb    w26, [sp, #0x4e]
00071cd0: add     x21, x21, #0x2e0 ; 0xa82e0 reloc 0xa7378
00071cd4: ldrb    w8, [sp, #0x4c]
00071cd8: cbnz    w8, #0x71d10
00071cdc: b       #0x71d28
00071ce0: ldr     x8, [x21] ; load 0xa82e0 reloc 0xa7378
00071ce4: ldrsw   x27, [sp, #0x14]
00071ce8: mov     x0, x21
00071cec: ldr     x8, [x8, #0x50]
00071cf0: blr     x8
00071cf4: adrp    x21, #0xa8000
00071cf8: cmp     x0, x27
00071cfc: add     x21, x21, #0x2e0 ; 0xa82e0 reloc 0xa7378
00071d00: b.ne    #0x71d08
00071d04: strb    w26, [sp, #0x4f]
00071d08: ldrb    w8, [sp, #0x4c]
00071d0c: cbz     w8, #0x71d28
00071d10: ldrb    w8, [sp, #0x4d]
00071d14: cbz     w8, #0x71d28
00071d18: ldrb    w8, [sp, #0x4e]
00071d1c: cbz     w8, #0x71d28
00071d20: ldrb    w8, [sp, #0x4f]
00071d24: cbnz    w8, #0x71e18
00071d28: ldr     x8, [x21] ; load 0xa82e0 reloc 0xa7378
00071d2c: ldrsw   x27, [sp, #0x14]
00071d30: mov     x0, x21
00071d34: ldr     x8, [x8, #0x48]
00071d38: blr     x8
00071d3c: cmp     x0, x27
00071d40: b.ne    #0x71d4c
00071d44: strb    w26, [sp, #0x52]
00071d48: b       #0x71d6c
00071d4c: ldr     x8, [x21] ; load 0xa82e0 reloc 0xa7378
00071d50: ldrsw   x27, [sp, #0x14]
00071d54: mov     x0, x21
00071d58: ldr     x8, [x8, #0x50]
00071d5c: blr     x8
00071d60: cmp     x0, x27
00071d64: b.ne    #0x71d6c
00071d68: strb    w26, [sp, #0x53]
00071d6c: ldrb    w8, [sp, #0x50]
00071d70: adrp    x21, #0xa8000
00071d74: add     x21, x21, #0x2d8 ; 0xa82d8 reloc 0xa72c8
00071d78: cbz     w8, #0x71a58
00071d7c: ldrb    w8, [sp, #0x51]
00071d80: cbz     w8, #0x71a58
00071d84: ldrb    w8, [sp, #0x52]
00071d88: cbz     w8, #0x71a58
00071d8c: ldrb    w8, [sp, #0x53]
00071d90: cbz     w8, #0x71a58
00071d94: adrp    x19, #0xa8000
00071d98: mov     w3, #2
00071d9c: add     x19, x19, #0x2e0 ; 0xa82e0 reloc 0xa7378
00071da0: b       #0x71e2c
00071da4: adrp    x1, #0x89000
00071da8: adrp    x2, #0x89000
00071dac: add     x1, x1, #0x207 ; 0x89207 'offset_probe'
00071db0: add     x2, x2, #0x1cd ; 0x891cd 'region_space_clear_addr null'
00071db4: mov     w0, #6
00071db8: bl      #0x11cc0 ; PLT reloc __android_log_print
00071dbc: b       #0x71de0
00071dc0: adrp    x1, #0x89000
00071dc4: adrp    x2, #0x89000
00071dc8: add     x1, x1, #0x207 ; 0x89207 'offset_probe'
00071dcc: add     x2, x2, #0x15d ; 0x8915d 'search memory[%p,%p]'
00071dd0: mov     w0, #6
00071dd4: mov     x3, x20
00071dd8: mov     x4, x23
00071ddc: bl      #0x11cc0 ; PLT reloc __android_log_print
00071de0: mov     x19, xzr
00071de4: ldr     x8, [x28, #0x28]
00071de8: ldr     x9, [sp, #0x58]
00071dec: cmp     x8, x9
00071df0: b.ne    #0x71e48
00071df4: mov     x0, x19
00071df8: ldp     x29, x30, [sp, #0xb0]
00071dfc: ldp     x20, x19, [sp, #0xa0]
00071e00: ldp     x22, x21, [sp, #0x90]
00071e04: ldp     x24, x23, [sp, #0x80]
00071e08: ldp     x26, x25, [sp, #0x70]
00071e0c: ldp     x28, x27, [sp, #0x60]
00071e10: add     sp, sp, #0xc0
00071e14: ret
00071e18: adrp    x19, #0xa8000
00071e1c: mov     w3, #1
00071e20: add     x19, x19, #0x2d8 ; 0xa82d8 reloc 0xa72c8
00071e24: b       #0x71e2c
00071e28: mov     w3, wzr
00071e2c: adrp    x1, #0x89000
00071e30: adrp    x2, #0x89000
00071e34: add     x1, x1, #0x207 ; 0x89207 'offset_probe'
00071e38: add     x2, x2, #0x1ea ; 0x891ea 'match target:%d'
00071e3c: mov     w0, #3
00071e40: bl      #0x11cc0 ; PLT reloc __android_log_print
00071e44: b       #0x71de4
00071e48: bl      #0x12270 ; PLT reloc __stack_chk_fail
