
Binary: file format elf64-littleaarch64

Disassembly of section .text:

000000000062e5ec <_ZN3art2gc10accounting11SpaceBitmapILm8EEC2ERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEONS_6MemMapEPmmPKvm>:
  62e5ec:      	paciasp
  62e5f0:      	sub	sp, sp, #0x80
  62e5f4:      	stp	x29, x30, [sp, #0x20]
  62e5f8:      	stp	x28, x27, [sp, #0x30]
  62e5fc:      	stp	x26, x25, [sp, #0x40]
  62e600:      	stp	x24, x23, [sp, #0x50]
  62e604:      	stp	x22, x21, [sp, #0x60]
  62e608:      	stp	x20, x19, [sp, #0x70]
  62e60c:      	add	x29, sp, #0x20
  62e610:      	mrs	x8, TPIDR_EL0
  62e614:      	mov	x22, x1
  62e618:      	mov	x1, x2
  62e61c:      	str	x8, [sp, #0x8]
  62e620:      	mov	x23, x6
  62e624:      	mov	x24, x5
  62e628:      	ldr	x8, [x8, #0x28]
  62e62c:      	mov	x20, x4
  62e630:      	mov	x21, x3
  62e634:      	mov	x19, x0
  62e638:      	stur	x8, [x29, #-0x8]
  62e63c:      	bl	0xd60400 <_ZN3art6MemMapC1EOS0_@plt>
  62e640:      	add	x8, x23, x24
  62e644:      	stp	x21, x20, [x19, #0x48]
  62e648:      	stp	x24, x8, [x19, #0x58]
  62e64c:      	ldrb	w8, [x22]
  62e650:      	tbnz	w8, #0x0, 0x62e668 <_ZN3art2gc10accounting11SpaceBitmapILm8EEC2ERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEONS_6MemMapEPmmPKvm+0x7c>
  62e654:      	ldr	x8, [x22, #0x10]
  62e658:      	ldr	q0, [x22]
  62e65c:      	stur	x8, [x19, #0x78]
  62e660:      	stur	q0, [x19, #0x68]
  62e664:      	b	0x62e678 <_ZN3art2gc10accounting11SpaceBitmapILm8EEC2ERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEONS_6MemMapEPmmPKvm+0x8c>
  62e668:      	ldp	x2, x1, [x22, #0x8]
  62e66c:      	add	x0, x19, #0x68
  62e670:      	bl	0x5fc200 <_ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE25__init_copy_ctor_externalEPKcm>
  62e674:      	ldr	x21, [x19, #0x48]
  62e678:      	cbz	x21, 0x62e7ac <_ZN3art2gc10accounting11SpaceBitmapILm8EEC2ERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEONS_6MemMapEPmmPKvm+0x1c0>
  62e67c:      	cbz	x20, 0x62e6b8 <_ZN3art2gc10accounting11SpaceBitmapILm8EEC2ERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEONS_6MemMapEPmmPKvm+0xcc>
  62e680:      	ldr	x8, [sp, #0x8]
  62e684:      	ldr	x8, [x8, #0x28]
  62e688:      	ldur	x9, [x29, #-0x8]
  62e68c:      	cmp	x8, x9
  62e690:      	b.ne	0x62e850 <_ZN3art2gc10accounting11SpaceBitmapILm8EEC2ERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEONS_6MemMapEPmmPKvm+0x264>
  62e694:      	ldp	x20, x19, [sp, #0x70]
  62e698:      	ldp	x22, x21, [sp, #0x60]
  62e69c:      	ldp	x24, x23, [sp, #0x50]
  62e6a0:      	ldp	x26, x25, [sp, #0x40]
  62e6a4:      	ldp	x28, x27, [sp, #0x30]
  62e6a8:      	ldp	x29, x30, [sp, #0x20]
  62e6ac:      	add	sp, sp, #0x80
  62e6b0:      	autiasp
  62e6b4:      	ret
  62e6b8:      	adrp	x20, 0xe9000 <.str.16.llvm.12451053423507216601+0x622>
  62e6bc:      	add	x20, x20, #0x220
  62e6c0:      	adrp	x21, 0xc2000 <.str.3.llvm.5294993930107823311+0x272>
  62e6c4:      	add	x21, x21, #0x852
  62e6c8:      	adrp	x22, 0xe0000 <.str.1.llvm.3108082989178328102+0x2ff>
  62e6cc:      	add	x22, x22, #0xcf0
  62e6d0:      	adrp	x23, 0xaf000 <.str.6.llvm.5294993930107823311+0x1f2>
  62e6d4:      	add	x23, x23, #0x726
  62e6d8:      	adrp	x24, 0xcd000 <.str.53.llvm.15349435720776883796+0x86>
  62e6dc:      	add	x24, x24, #0xa56
  62e6e0:      	adrp	x25, 0xac000 <.str.161.llvm.11382447859366526032+0x3ea>
  62e6e4:      	add	x25, x25, #0xbfe
  62e6e8:      	adrp	x26, 0xe6000 <.str.8.llvm.5294993930107823311+0x1e>
  62e6ec:      	add	x26, x26, #0x841
  62e6f0:      	adrp	x27, 0xfc000 <.str.8.llvm.1361002470434697266+0x331>
  62e6f4:      	add	x27, x27, #0x6d0
  62e6f8:      	adrp	x28, 0xe3000 <.str.179.llvm.15807031110028088274+0x4bc>
  62e6fc:      	add	x28, x28, #0xa38
  62e700:      	add	x0, sp, #0x10
  62e704:      	mov	x1, x20
  62e708:      	mov	w2, #0x4c               // =76
  62e70c:      	mov	w3, #0x6                // =6
  62e710:      	mov	x4, xzr
  62e714:      	mov	w5, #-0x1               // =-1
  62e718:      	bl	0xd5ea70 <_ZN7android4base10LogMessageC1EPKcjNS0_11LogSeverityES3_i@plt>
  62e71c:      	add	x0, sp, #0x10
  62e720:      	bl	0xd5ea80 <_ZN7android4base10LogMessage6streamEv@plt>
  62e724:      	mov	x1, x21
  62e728:      	mov	w2, #0xe                // =14
  62e72c:      	bl	0x4040c8 <_ZNSt3__124__put_character_sequenceB8ne200000IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m>
  62e730:      	mov	x1, x22
  62e734:      	mov	w2, #0xb                // =11
  62e738:      	bl	0x4040c8 <_ZNSt3__124__put_character_sequenceB8ne200000IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m>
  62e73c:      	mov	x1, x23
  62e740:      	mov	w2, #0x1                // =1
  62e744:      	bl	0x4040c8 <_ZNSt3__124__put_character_sequenceB8ne200000IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m>
  62e748:      	mov	x1, x24
  62e74c:      	mov	w2, #0x2                // =2
  62e750:      	bl	0x4040c8 <_ZNSt3__124__put_character_sequenceB8ne200000IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m>
  62e754:      	mov	x1, x23
  62e758:      	mov	w2, #0x1                // =1
  62e75c:      	bl	0x4040c8 <_ZNSt3__124__put_character_sequenceB8ne200000IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m>
  62e760:      	mov	x1, x25
  62e764:      	mov	w2, #0x2                // =2
  62e768:      	bl	0x4040c8 <_ZNSt3__124__put_character_sequenceB8ne200000IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m>
  62e76c:      	mov	x1, x26
  62e770:      	mov	w2, #0xe                // =14
  62e774:      	bl	0x4040c8 <_ZNSt3__124__put_character_sequenceB8ne200000IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m>
  62e778:      	mov	x1, xzr
  62e77c:      	bl	0xd5ea90 <_ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEm@plt>
  62e780:      	mov	x1, x27
  62e784:      	mov	w2, #0x5                // =5
  62e788:      	bl	0x4040c8 <_ZNSt3__124__put_character_sequenceB8ne200000IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m>
  62e78c:      	mov	w1, wzr
  62e790:      	bl	0xd5ebf0 <_ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEj@plt>
  62e794:      	mov	x1, x28
  62e798:      	mov	w2, #0x2                // =2
  62e79c:      	bl	0x4040c8 <_ZNSt3__124__put_character_sequenceB8ne200000IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m>
  62e7a0:      	add	x0, sp, #0x10
  62e7a4:      	bl	0xd5eaa0 <_ZN7android4base10LogMessageD1Ev@plt>
  62e7a8:      	b	0x62e700 <_ZN3art2gc10accounting11SpaceBitmapILm8EEC2ERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEONS_6MemMapEPmmPKvm+0x114>
  62e7ac:      	adrp	x1, 0xe9000 <.str.16.llvm.12451053423507216601+0x622>
  62e7b0:      	add	x1, x1, #0x220
  62e7b4:      	add	x0, sp, #0x10
  62e7b8:      	mov	w2, #0x4b               // =75
  62e7bc:      	mov	w3, #0x6                // =6
  62e7c0:      	mov	x4, xzr
  62e7c4:      	mov	w5, #-0x1               // =-1
  62e7c8:      	bl	0xd5ea70 <_ZN7android4base10LogMessageC1EPKcjNS0_11LogSeverityES3_i@plt>
  62e7cc:      	add	x0, sp, #0x10
  62e7d0:      	bl	0xd5ea80 <_ZN7android4base10LogMessage6streamEv@plt>
  62e7d4:      	adrp	x1, 0xb2000 <.str.4.llvm.18346605400851311032+0x7f2>
  62e7d8:      	add	x1, x1, #0xb0
  62e7dc:      	mov	w2, #0x26               // =38
  62e7e0:      	bl	0x4040c8 <_ZNSt3__124__put_character_sequenceB8ne200000IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m>
  62e7e4:      	adrp	x1, 0xaf000 <.str.6.llvm.5294993930107823311+0x1f2>
  62e7e8:      	add	x1, x1, #0x726
  62e7ec:      	mov	w2, #0x1                // =1
  62e7f0:      	bl	0x4040c8 <_ZNSt3__124__put_character_sequenceB8ne200000IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m>
  62e7f4:      	add	x0, sp, #0x10
  62e7f8:      	bl	0xd5eaa0 <_ZN7android4base10LogMessageD1Ev@plt>
  62e7fc:      	b	0x62e67c <_ZN3art2gc10accounting11SpaceBitmapILm8EEC2ERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEONS_6MemMapEPmmPKvm+0x90>
  62e800:      	b	0x62e810 <_ZN3art2gc10accounting11SpaceBitmapILm8EEC2ERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEONS_6MemMapEPmmPKvm+0x224>
  62e804:      	b	0x62e818 <_ZN3art2gc10accounting11SpaceBitmapILm8EEC2ERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEONS_6MemMapEPmmPKvm+0x22c>
  62e808:      	mov	x20, x0
  62e80c:      	b	0x62e82c <_ZN3art2gc10accounting11SpaceBitmapILm8EEC2ERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEONS_6MemMapEPmmPKvm+0x240>
  62e810:      	mov	x20, x0
  62e814:      	b	0x62e824 <_ZN3art2gc10accounting11SpaceBitmapILm8EEC2ERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEONS_6MemMapEPmmPKvm+0x238>
  62e818:      	mov	x20, x0
  62e81c:      	add	x0, sp, #0x10
  62e820:      	bl	0xd5eaa0 <_ZN7android4base10LogMessageD1Ev@plt>
  62e824:      	ldurb	w8, [x19, #0x68]
  62e828:      	tbnz	w8, #0x0, 0x62e854 <_ZN3art2gc10accounting11SpaceBitmapILm8EEC2ERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEONS_6MemMapEPmmPKvm+0x268>
  62e82c:      	mov	x0, x19
  62e830:      	bl	0xd603b0 <_ZN3art6MemMapD1Ev@plt>
  62e834:      	ldr	x8, [sp, #0x8]
  62e838:      	ldr	x8, [x8, #0x28]
  62e83c:      	ldur	x9, [x29, #-0x8]
  62e840:      	cmp	x8, x9
  62e844:      	b.ne	0x62e850 <_ZN3art2gc10accounting11SpaceBitmapILm8EEC2ERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEONS_6MemMapEPmmPKvm+0x264>
  62e848:      	mov	x0, x20
  62e84c:      	bl	0xd63f70 <_Unwind_Resume@plt>
  62e850:      	bl	0xd63ff0 <__stack_chk_fail@plt>
  62e854:      	ldr	x8, [x19, #0x68]
  62e858:      	ldr	x0, [x19, #0x78]
  62e85c:      	and	x1, x8, #0xfffffffffffffffe
  62e860:      	bl	0xd5eae0 <_ZdlPvm@plt>
  62e864:      	b	0x62e82c <_ZN3art2gc10accounting11SpaceBitmapILm8EEC2ERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEEONS_6MemMapEPmmPKvm+0x240>
