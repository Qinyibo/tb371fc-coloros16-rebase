
Binary: file format elf64-littleaarch64

Disassembly of section .text:

00000000006b7a58 <_ZNK3art2gc10accounting11SpaceBitmapILm8EE16VisitMarkedRangeILb0ERKZNS0_9collector17ConcurrentCopying12CopyingPhaseEvE3$_0EEvmmOT0_.__uniq.219178288367021339109957061695789229157>:
  6b7a58:      	paciasp
  6b7a5c:      	sub	sp, sp, #0x70
  6b7a60:      	stp	x29, x30, [sp, #0x10]
  6b7a64:      	stp	x28, x27, [sp, #0x20]
  6b7a68:      	stp	x26, x25, [sp, #0x30]
  6b7a6c:      	stp	x24, x23, [sp, #0x40]
  6b7a70:      	stp	x22, x21, [sp, #0x50]
  6b7a74:      	stp	x20, x19, [sp, #0x60]
  6b7a78:      	add	x29, sp, #0x10
  6b7a7c:      	ldr	x9, [x0, #0x58]
  6b7a80:      	ldr	x10, [x0, #0x48]
  6b7a84:      	mov	x12, #-0x1              // =-1
  6b7a88:      	sub	x8, x1, x9
  6b7a8c:      	sub	x22, x2, x9
  6b7a90:      	lsr	x25, x8, #9
  6b7a94:      	lsr	x11, x8, #3
  6b7a98:      	ubfx	x23, x22, #3, #6
  6b7a9c:      	add	x10, x10, x25, lsl #3
  6b7aa0:      	cmp	x25, x22, lsr #9
  6b7aa4:      	ldar	x9, [x10]
  6b7aa8:      	lsl	x10, x12, x11
  6b7aac:      	and	x26, x10, x9
  6b7ab0:      	b.hs	0x6b7c58 <_ZNK3art2gc10accounting11SpaceBitmapILm8EE16VisitMarkedRangeILb0ERKZNS0_9collector17ConcurrentCopying12CopyingPhaseEvE3$_0EEvmmOT0_.__uniq.219178288367021339109957061695789229157+0x200>
