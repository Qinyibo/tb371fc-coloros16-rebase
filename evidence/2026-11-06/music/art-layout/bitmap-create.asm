
Binary: file format elf64-littleaarch64

Disassembly of section .text:

000000000062e2c8 <_ZN3art2gc10accounting11SpaceBitmapILm8EE6CreateERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEPhm>:
  62e2c8:      	paciasp
  62e2cc:      	sub	sp, sp, #0xc0
  62e2d0:      	stp	x29, x30, [sp, #0x80]
  62e2d4:      	str	x23, [sp, #0x90]
  62e2d8:      	stp	x22, x21, [sp, #0xa0]
  62e2dc:      	stp	x20, x19, [sp, #0xb0]
  62e2e0:      	add	x29, sp, #0x80
  62e2e4:      	mrs	x23, TPIDR_EL0
  62e2e8:      	mov	x19, x8
  62e2ec:      	movi	v0.2d, #0000000000000000
  62e2f0:      	ldr	x8, [x23, #0x28]
  62e2f4:      	mov	x21, x2
  62e2f8:      	mov	x22, x1
  62e2fc:      	mov	x20, x0
  62e300:      	add	x9, x2, #0x1ff
  62e304:      	stur	x8, [x29, #-0x8]
  62e308:      	lsr	x9, x9, #6
  62e30c:      	ldrb	w8, [x0]
  62e310:      	ldr	x10, [x0, #0x10]
  62e314:      	stp	xzr, xzr, [x29, #-0x20]
  62e318:      	stur	xzr, [x29, #-0x10]
  62e31c:      	tst	w8, #0x1
  62e320:      	str	xzr, [sp, #0x50]
  62e324:      	csinc	x0, x10, x0, ne
  62e328:      	stp	q0, q0, [sp, #0x10]
  62e32c:      	stp	q0, q0, [sp, #0x30]
  62e330:      	mov	w10, #0x1               // =1
  62e334:      	add	x8, sp, #0x10
  62e338:      	and	x2, x9, #0x3fffffffffffff8
  62e33c:      	sub	x7, x29, #0x20
  62e340:      	mov	x1, xzr
  62e344:      	mov	w3, #0x3                // =3
  62e348:      	mov	w4, wzr
  62e34c:      	mov	w5, wzr
  62e350:      	mov	x6, xzr
  62e354:      	strb	w10, [sp]
  62e358:      	bl	0xd60410 <_ZN3art6MemMap12MapAnonymousEPKcPhmibbPS0_PNSt3__112basic_stringIcNS5_11char_traitsIcEENS5_9allocatorIcEEEEb@plt>
  62e35c:      	ldr	x8, [sp, #0x40]
  62e360:      	cbz	x8, 0x62e3cc <_ZN3art2gc10accounting11SpaceBitmapILm8EE6CreateERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEPhm+0x104>
  62e364:      	add	x1, sp, #0x10
  62e368:      	mov	x8, x19
  62e36c:      	mov	x0, x20
  62e370:      	mov	x2, x22
  62e374:      	mov	x3, x21
  62e378:      	bl	0x62e4d4 <_ZN3art2gc10accounting11SpaceBitmapILm8EE16CreateFromMemMapERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEONS_6MemMapEPhm>
  62e37c:      	add	x0, sp, #0x10
  62e380:      	bl	0xd603b0 <_ZN3art6MemMapD1Ev@plt>
  62e384:      	ldurb	w8, [x29, #-0x20]
  62e388:      	tbnz	w8, #0x0, 0x62e3b8 <_ZN3art2gc10accounting11SpaceBitmapILm8EE6CreateERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEPhm+0xf0>
  62e38c:      	ldr	x8, [x23, #0x28]
  62e390:      	ldur	x9, [x29, #-0x8]
  62e394:      	cmp	x8, x9
  62e398:      	b.ne	0x62e4bc <_ZN3art2gc10accounting11SpaceBitmapILm8EE6CreateERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEPhm+0x1f4>
  62e39c:      	ldp	x20, x19, [sp, #0xb0]
  62e3a0:      	ldr	x23, [sp, #0x90]
  62e3a4:      	ldp	x22, x21, [sp, #0xa0]
  62e3a8:      	ldp	x29, x30, [sp, #0x80]
  62e3ac:      	add	sp, sp, #0xc0
  62e3b0:      	autiasp
  62e3b4:      	ret
  62e3b8:      	ldur	x8, [x29, #-0x20]
  62e3bc:      	ldur	x0, [x29, #-0x10]
  62e3c0:      	and	x1, x8, #0xfffffffffffffffe
  62e3c4:      	bl	0xd5eae0 <_ZdlPvm@plt>
  62e3c8:      	b	0x62e38c <_ZN3art2gc10accounting11SpaceBitmapILm8EE6CreateERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEPhm+0xc4>
  62e3cc:      	mov	w0, #0x4                // =4
  62e3d0:      	mov	x1, xzr
  62e3d4:      	bl	0xd5eb20 <_ZN7android4base9ShouldLogENS0_11LogSeverityEPKc@plt>
  62e3d8:      	tbnz	w0, #0x0, 0x62e3f4 <_ZN3art2gc10accounting11SpaceBitmapILm8EE6CreateERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEPhm+0x12c>
  62e3dc:      	movi	v0.2d, #0000000000000000
  62e3e0:      	stp	q0, q0, [x19]
  62e3e4:      	stp	q0, q0, [x19, #0x20]
  62e3e8:      	stp	q0, q0, [x19, #0x40]
  62e3ec:      	stp	q0, q0, [x19, #0x60]
  62e3f0:      	b	0x62e37c <_ZN3art2gc10accounting11SpaceBitmapILm8EE6CreateERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEPhm+0xb4>
  62e3f4:      	bl	0xd5eb30 <__errno@plt>
  62e3f8:      	ldr	w22, [x0]
  62e3fc:      	mov	x21, x0
  62e400:      	adrp	x1, 0xe9000 <.str.16.llvm.12451053423507216601+0x622>
  62e404:      	add	x1, x1, #0x220
  62e408:      	add	x0, sp, #0x8
  62e40c:      	mov	w2, #0x5f               // =95
  62e410:      	mov	w3, #0x4                // =4
  62e414:      	mov	x4, xzr
  62e418:      	mov	w5, #-0x1               // =-1
  62e41c:      	bl	0xd5ea70 <_ZN7android4base10LogMessageC1EPKcjNS0_11LogSeverityES3_i@plt>
  62e420:      	add	x0, sp, #0x8
  62e424:      	bl	0xd5ea80 <_ZN7android4base10LogMessage6streamEv@plt>
  62e428:      	adrp	x1, 0xde000 <.str.llvm.7791326160212776137+0x519>
  62e42c:      	add	x1, x1, #0x3a3
  62e430:      	mov	w2, #0x1a               // =26
  62e434:      	bl	0x4040c8 <_ZNSt3__124__put_character_sequenceB8ne200000IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m>
  62e438:      	mov	x1, x20
  62e43c:      	bl	0x41b428 <_ZNSt3__1lsB8ne200000IcNS_11char_traitsIcEENS_9allocatorIcEEEERNS_13basic_ostreamIT_T0_EES9_RKNS_12basic_stringIS6_S7_T1_EE>
  62e440:      	adrp	x1, 0xf6000 <.str.13.llvm.3621554912258221549+0x299>
  62e444:      	add	x1, x1, #0xd0c
  62e448:      	mov	w2, #0x2                // =2
  62e44c:      	bl	0x4040c8 <_ZNSt3__124__put_character_sequenceB8ne200000IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m>
  62e450:      	sub	x1, x29, #0x20
  62e454:      	bl	0x41b428 <_ZNSt3__1lsB8ne200000IcNS_11char_traitsIcEENS_9allocatorIcEEEERNS_13basic_ostreamIT_T0_EES9_RKNS_12basic_stringIS6_S7_T1_EE>
  62e458:      	add	x0, sp, #0x8
  62e45c:      	bl	0xd5eaa0 <_ZN7android4base10LogMessageD1Ev@plt>
  62e460:      	str	w22, [x21]
  62e464:      	b	0x62e3dc <_ZN3art2gc10accounting11SpaceBitmapILm8EE6CreateERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEPhm+0x114>
  62e468:      	mov	x19, x0
  62e46c:      	b	0x62e47c <_ZN3art2gc10accounting11SpaceBitmapILm8EE6CreateERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEPhm+0x1b4>
  62e470:      	mov	x19, x0
  62e474:      	add	x0, sp, #0x8
  62e478:      	bl	0xd5eaa0 <_ZN7android4base10LogMessageD1Ev@plt>
  62e47c:      	str	w22, [x21]
  62e480:      	b	0x62e48c <_ZN3art2gc10accounting11SpaceBitmapILm8EE6CreateERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEPhm+0x1c4>
  62e484:      	b	0x62e488 <_ZN3art2gc10accounting11SpaceBitmapILm8EE6CreateERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEPhm+0x1c0>
  62e488:      	mov	x19, x0
  62e48c:      	add	x0, sp, #0x10
  62e490:      	bl	0xd603b0 <_ZN3art6MemMapD1Ev@plt>
  62e494:      	b	0x62e49c <_ZN3art2gc10accounting11SpaceBitmapILm8EE6CreateERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEPhm+0x1d4>
  62e498:      	mov	x19, x0
  62e49c:      	ldurb	w8, [x29, #-0x20]
  62e4a0:      	tbnz	w8, #0x0, 0x62e4c0 <_ZN3art2gc10accounting11SpaceBitmapILm8EE6CreateERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEPhm+0x1f8>
  62e4a4:      	ldr	x8, [x23, #0x28]
  62e4a8:      	ldur	x9, [x29, #-0x8]
  62e4ac:      	cmp	x8, x9
  62e4b0:      	b.ne	0x62e4bc <_ZN3art2gc10accounting11SpaceBitmapILm8EE6CreateERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEPhm+0x1f4>
  62e4b4:      	mov	x0, x19
  62e4b8:      	bl	0xd63f70 <_Unwind_Resume@plt>
  62e4bc:      	bl	0xd63ff0 <__stack_chk_fail@plt>
  62e4c0:      	ldur	x8, [x29, #-0x20]
  62e4c4:      	ldur	x0, [x29, #-0x10]
  62e4c8:      	and	x1, x8, #0xfffffffffffffffe
  62e4cc:      	bl	0xd5eae0 <_ZdlPvm@plt>
  62e4d0:      	b	0x62e4a4 <_ZN3art2gc10accounting11SpaceBitmapILm8EE6CreateERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEPhm+0x1dc>
