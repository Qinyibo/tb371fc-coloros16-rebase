
.\scheduler-compat\gpu-floor-native-v7\sameboot-aba\libart.so:	file format elf64-littleaarch64

Disassembly of section .text:

0000000000a502b8 <_ZN3art2gc5space11RegionSpace5ClearEv>:
  a502b8:      	paciasp
  a502bc:      	sub	sp, sp, #0x50
  a502c0:      	stp	x29, x30, [sp, #0x20]
  a502c4:      	stp	x22, x21, [sp, #0x30]
  a502c8:      	stp	x20, x19, [sp, #0x40]
  a502cc:      	add	x29, sp, #0x20
  a502d0:      	mrs	x20, TPIDR_EL0
  a502d4:      	adrp	x9, 0xe35000 <_DYNAMIC+0x38>
  a502d8:      	mov	x19, x0
  a502dc:      	ldr	x8, [x20, #0x28]
  a502e0:      	ldr	x9, [x9, #0x2b8]
  a502e4:      	stur	x8, [x29, #-0x8]
  a502e8:      	ldrb	w8, [x9]
  a502ec:      	cmp	w8, #0x1
  a502f0:      	b.ne	0xa50394 <_ZN3art2gc5space11RegionSpace5ClearEv+0xdc>
  a502f4:      	mrs	x8, TPIDR_EL0
  a502f8:      	ldr	x1, [x8, #0x38]
  a502fc:      	add	x0, x19, #0x210
  a50300:      	stp	x1, x0, [sp, #0x8]
  a50304:      	bl	0xd5eb40 <_ZN3art5Mutex13ExclusiveLockEPNS_6ThreadE@plt>
  a50308:      	ldr	x8, [x19, #0x248]
  a5030c:      	cbz	x8, 0xa5034c <_ZN3art2gc5space11RegionSpace5ClearEv+0x94>
  a50310:      	mov	x21, xzr
  a50314:      	mov	x22, xzr
  a50318:      	ldr	x8, [x19, #0x270]
  a5031c:      	add	x0, x8, x21
  a50320:      	ldrb	w8, [x0, #0x3e]
  a50324:      	cbz	w8, 0xa50334 <_ZN3art2gc5space11RegionSpace5ClearEv+0x7c>
  a50328:      	ldr	x8, [x19, #0x258]
  a5032c:      	sub	x8, x8, #0x1
  a50330:      	str	x8, [x19, #0x258]
  a50334:      	bl	0xa4fde0 <_ZN3art2gc5space11RegionSpace6Region5ClearEb>
  a50338:      	ldr	x8, [x19, #0x248]
  a5033c:      	add	x22, x22, #0x1
  a50340:      	add	x21, x21, #0x48
  a50344:      	cmp	x22, x8
  a50348:      	b.lo	0xa50318 <_ZN3art2gc5space11RegionSpace5ClearEv+0x60>
  a5034c:      	add	x8, x19, #0x2b8
  a50350:      	add	x0, sp, #0x8
  a50354:      	str	xzr, [x19, #0x290]
  a50358:      	str	x8, [x19, #0x298]
  a5035c:      	str	x8, [x19, #0x2a0]
  a50360:      	str	x8, [x19, #0x2a8]
  a50364:      	str	x8, [x19, #0x2b0]
  a50368:      	bl	0x5c71f8 <_ZN3art9MutexLockD2Ev>
  a5036c:      	ldr	x8, [x20, #0x28]
  a50370:      	ldur	x9, [x29, #-0x8]
  a50374:      	cmp	x8, x9
  a50378:      	b.ne	0xa503c0 <_ZN3art2gc5space11RegionSpace5ClearEv+0x108>
  a5037c:      	ldp	x20, x19, [sp, #0x40]
  a50380:      	ldp	x22, x21, [sp, #0x30]
  a50384:      	ldp	x29, x30, [sp, #0x20]
  a50388:      	add	sp, sp, #0x50
  a5038c:      	autiasp
  a50390:      	ret
  a50394:      	mov	x1, xzr
  a50398:      	b	0xa502fc <_ZN3art2gc5space11RegionSpace5ClearEv+0x44>
  a5039c:      	mov	x19, x0
  a503a0:      	add	x0, sp, #0x8
  a503a4:      	bl	0x5c71f8 <_ZN3art9MutexLockD2Ev>
  a503a8:      	ldr	x8, [x20, #0x28]
  a503ac:      	ldur	x9, [x29, #-0x8]
  a503b0:      	cmp	x8, x9
  a503b4:      	b.ne	0xa503c0 <_ZN3art2gc5space11RegionSpace5ClearEv+0x108>
  a503b8:      	mov	x0, x19
  a503bc:      	bl	0xd63f70 <_Unwind_Resume@plt>
  a503c0:      	bl	0xd63ff0 <__stack_chk_fail@plt>
