
Binary: file format elf64-littleaarch64

Disassembly of section .text:

000000000087e6b0 <_ZN3art2gc10accounting11SpaceBitmapILm8EE12SetHeapLimitEm>:
  87e6b0:      	bti	c
  87e6b4:      	ldp	x9, x8, [x0, #0x50]
  87e6b8:      	sub	x8, x1, x8
  87e6bc:      	lsr	x8, x8, #6
  87e6c0:      	and	x8, x8, #0x3fffffffffffff8
  87e6c4:      	cmp	x8, x9
  87e6c8:      	b.hs	0x87e6d0 <_ZN3art2gc10accounting11SpaceBitmapILm8EE12SetHeapLimitEm+0x20>
  87e6cc:      	str	x8, [x0, #0x50]
  87e6d0:      	str	x1, [x0, #0x60]
  87e6d4:      	ret
