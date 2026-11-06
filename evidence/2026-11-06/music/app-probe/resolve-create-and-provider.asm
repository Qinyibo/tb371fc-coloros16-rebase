Instruction range [0x6fed4, 0x700a4); symbol names omitted for stripped local functions.
0006fed4: sub     sp, sp, #0x50
0006fed8: stp     x24, x23, [sp, #0x10]
0006fedc: stp     x22, x21, [sp, #0x20]
0006fee0: stp     x20, x19, [sp, #0x30]
0006fee4: stp     x29, x30, [sp, #0x40]
0006fee8: add     x29, sp, #0x40
0006feec: adrp    x1, #0x88000
0006fef0: adrp    x2, #0x79000
0006fef4: add     x1, x1, #0x8e8 ; 0x888e8 'expand_helper'
0006fef8: add     x2, x2, #0xfde ; 0x79fde 'init'
0006fefc: mov     w0, #3
0006ff00: bl      #0x11cc0 ; PLT reloc __android_log_print
0006ff04: bl      #0x72588
0006ff08: tbz     w0, #0, #0x70000
0006ff0c: adrp    x0, #0x88000
0006ff10: add     x0, x0, #0x8f6 ; 0x888f6 '_ZN3art2gc4Heap8AddSpaceEPNS0_5space5SpaceE'
0006ff14: bl      #0x71064
0006ff18: adrp    x20, #0xaf000
0006ff1c: str     x0, [x20, #0x28]
0006ff20: adrp    x0, #0x88000
0006ff24: add     x0, x0, #0x922 ; 0x88922 '_ZN3art2gc4Heap11RemoveSpaceEPNS0_5space5SpaceE'
0006ff28: bl      #0x71064
0006ff2c: adrp    x21, #0xaf000
0006ff30: str     x0, [x21, #0x30]
0006ff34: adrp    x0, #0x88000
0006ff38: add     x0, x0, #0x952 ; 0x88952 '_ZN3art2gc10accounting11SpaceBitmapILm8EE6CreateERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEPhm'
0006ff3c: bl      #0x71064
0006ff40: adrp    x22, #0xaf000
0006ff44: adrp    x8, #0xaf000
0006ff48: str     x0, [x22, #0x38]
0006ff4c: str     x0, [x8, #0x40]
0006ff50: adrp    x0, #0x88000
0006ff54: add     x0, x0, #0x8a2 ; 0x888a2 '_ZN3art2gc4Heap7StartGCEPNS_6ThreadENS0_7GcCauseENS0_13CollectorTypeE'
0006ff58: bl      #0x71064
0006ff5c: adrp    x23, #0xaf000
0006ff60: str     x0, [x23, #0x20]
0006ff64: adrp    x0, #0x88000
0006ff68: add     x0, x0, #0x9c9 ; 0x889c9 '_ZN3art2gc4Heap8FinishGCEPNS_6ThreadENS0_9collector6GcTypeE'
0006ff6c: bl      #0x71064
0006ff70: adrp    x24, #0xaf000
0006ff74: str     x0, [x24, #0x48]
0006ff78: adrp    x0, #0x88000
0006ff7c: add     x0, x0, #0xa05 ; 0x88a05 '_ZN3art2gc4Heap8FinishGCEPNS_6ThreadENS0_9collector6GcTypeENS0_7GcCauseE'
0006ff80: bl      #0x71064
0006ff84: ldr     x3, [x23, #0x20]
0006ff88: ldr     x4, [x24, #0x48]
0006ff8c: adrp    x19, #0xaf000
0006ff90: adrp    x1, #0x88000
0006ff94: adrp    x2, #0x88000
0006ff98: mov     x5, x0
0006ff9c: str     x0, [x19, #0x50]
0006ffa0: add     x1, x1, #0x8e8 ; 0x888e8 'expand_helper'
0006ffa4: add     x2, x2, #0xa4e ; 0x88a4e 'heap start/stop gc:%p, %p, %p(hw)'
0006ffa8: mov     w0, #3
0006ffac: bl      #0x11cc0 ; PLT reloc __android_log_print
0006ffb0: ldr     x3, [x20, #0x28]
0006ffb4: ldr     x4, [x21, #0x30]
0006ffb8: ldr     x5, [x22, #0x38]
0006ffbc: ldr     x6, [x23, #0x20]
0006ffc0: ldr     x7, [x24, #0x48]
0006ffc4: cbz     x3, #0x70018
0006ffc8: cbz     x4, #0x70018
0006ffcc: cbz     x5, #0x70018
0006ffd0: cbz     x6, #0x70018
0006ffd4: cbnz    x7, #0x6ffe0
0006ffd8: ldr     x8, [x19, #0x50]
0006ffdc: cbz     x8, #0x7001c
0006ffe0: bl      #0x728a4
0006ffe4: tbz     w0, #0, #0x7006c
0006ffe8: bl      #0x71e4c
0006ffec: adrp    x8, #0xae000
0006fff0: str     x0, [x8, #0xff8]
0006fff4: cbz     x0, #0x70080
0006fff8: mov     w0, #1
0006fffc: b       #0x70054
00070000: adrp    x1, #0x88000
00070004: adrp    x2, #0x88000
00070008: add     x1, x1, #0x8e8 ; 0x888e8 'expand_helper'
0007000c: add     x2, x2, #0x834 ; 0x88834 'suspend_all init fail'
00070010: mov     w0, #6
00070014: b       #0x7004c
00070018: ldr     x8, [x19, #0x50]
0007001c: adrp    x19, #0x88000
00070020: add     x19, x19, #0x8e8 ; 0x888e8 'expand_helper'
00070024: adrp    x2, #0x88000
00070028: add     x2, x2, #0xa70 ; 0x88a70 'find sym fail:%p, %p, %p, %p, %p, %p'
0007002c: mov     w0, #6
00070030: mov     x1, x19
00070034: str     x8, [sp]
00070038: bl      #0x11cc0 ; PLT reloc __android_log_print
0007003c: adrp    x2, #0x88000
00070040: add     x2, x2, #0x84a ; 0x8884a 'found sym fail'
00070044: mov     w0, #6
00070048: mov     x1, x19
0007004c: bl      #0x11cc0 ; PLT reloc __android_log_print
00070050: mov     w0, wzr
00070054: ldp     x29, x30, [sp, #0x40]
00070058: ldp     x20, x19, [sp, #0x30]
0007005c: ldp     x22, x21, [sp, #0x20]
00070060: ldp     x24, x23, [sp, #0x10]
00070064: add     sp, sp, #0x50
00070068: ret
0007006c: adrp    x1, #0x88000
00070070: adrp    x2, #0x88000
00070074: add     x1, x1, #0x8e8 ; 0x888e8 'expand_helper'
00070078: add     x2, x2, #0x859 ; 0x88859 'tlab_fix init fail'
0007007c: b       #0x70010
00070080: bl      #0x71084
00070084: adrp    x1, #0x88000
00070088: adrp    x2, #0x88000
0007008c: mov     w3, w0
00070090: add     x1, x1, #0x8e8 ; 0x888e8 'expand_helper'
00070094: add     x2, x2, #0x86c ; 0x8886c '[-]unknown offsets, api level: %d'
00070098: mov     w0, #6
0007009c: bl      #0x11cc0 ; PLT reloc __android_log_print
000700a0: b       #0x70050
