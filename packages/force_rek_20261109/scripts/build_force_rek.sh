#!/bin/bash
set -euo pipefail
TREE=/work/r108-src
OUT=/work/r108-out
export PATH="/usr/lib/llvm-21/bin:$PATH"
export KBUILD_BUILD_USER=tb371fc-offline
export KBUILD_BUILD_HOST=r108-force-rek
export KBUILD_BUILD_VERSION=45
export KBUILD_BUILD_TIMESTAMP="Mon Nov 09 2026 18:25:00 +0800"
FLAGS="-Wno-error -Wno-error=strict-prototypes -Wno-error=implicit-int -Wno-error=incompatible-pointer-types -Wno-error=date-time -include $TREE/drivers/staging/fw-api/fw/p226_compat.h"
# Ensure config exists; do not overwrite existing out config if present
if [ ! -f "$OUT/.config" ]; then
  mkdir -p "$OUT"
  cp "$TREE/build/tb371fc/kernel43.config" "$OUT/.config"
fi
echo "clang=$(clang --version | head -1)"
echo "building Image into $OUT ..."
make -C "$TREE" --output-sync=target -j"$(nproc)" O="$OUT" ARCH=arm64 CC=clang CLANG_TRIPLE=aarch64-linux-gnu- CROSS_COMPILE=aarch64-linux-gnu- AS=aarch64-linux-gnu-as LOCALVERSION= KCFLAGS="$FLAGS" DYNAMIC_SINGLE_CHIP=qca6390 Image
ls -la "$OUT/arch/arm64/boot/Image"
sha256sum "$OUT/arch/arm64/boot/Image"
strings "$OUT/arch/arm64/boot/Image" | grep -E 'R10x_FORCE_REK|r108-force-rek|R108_RESX' | head -20
