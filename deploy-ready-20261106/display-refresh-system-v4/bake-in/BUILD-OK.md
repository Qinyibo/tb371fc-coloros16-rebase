# BUILD-OK my_product-bakein.img

- Timestamp Asia/Hong_Kong: 2026-11-06 16:18:45
- Distro: WSL TB371FC-Builder (NOT Ubuntu-24.04)
- Donor: D:\TB371FC-release\clean-rebase-20261104\donor-images\my_product.img
- Extract: fsck.erofs --extract on Linux ext4 /home/ubuntu/work-bakein-20261106 (NTFS case-collision avoided)
- Patch: python3 rom-stage/patch_my_product_tree.py
- Tree XML MD5: 35db38f8c85758c372546c707513642c (UTF-8 no BOM)
- mkfs: mkfs.erofs -zlz4hc,9 -b4096 (donor compr_algs=lz4)
- OUT: D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\display-refresh-system-v4\bake-in\my_product-bakein.img
- Size bytes: 2228305920
- SHA256: 246c901975dc5eb84c16e16aadcfecb5bcaab790369fe405dc78d1a8c9c479e5
- MD5: b06dce8a893d3eccd755a4cb4836f65c
- Inodes: 3645 (matches donor)
- hardware_success_claimed: false
- Flash: not done in this step yet
## Flash attempt 2026-11-06 Asia/Hong_Kong
- Result: NOT flashed — fastbootd cannot open my_product / my_product_a
- See FLASH-BLOCKER.md and flash-probe-20261106.log
- Device recovered to Android system OK
