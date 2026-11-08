#!/usr/bin/env bash
# Rebuild my_product.img (EROFS). Linux only. Qin WSL CORRUPTED 2026-11-06.
set -euo pipefail
if [ $# -ne 2 ]; then echo usage: rebuild_my_product_erofs.sh TREE OUT; exit 2; fi
TREE=$1
OUT=$2
command -v mkfs.erofs >/dev/null || { echo need mkfs.erofs; exit 1; }
mkfs.erofs -zlz4hc,9 -b4096 $OUT $TREE
echo built
ls -la $OUT
sha256sum $OUT
