#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
out="$r/apex-ext4-prototype/com.android.runtime"
keys="$r/private-signing/apex/com.android.runtime"
avb=/mnt/d/vivo/新建文件夹/中轴门/TB371FC_ColorOS16/tools/aosp-build-tools/android16/linux-x86/bin/avbtool
export TMPDIR="$r/temp"
umask 077
mkdir -p "$keys"
if test ! -f "$keys/payload.pem"; then
 openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out "$keys/payload.pem" > "$keys/payload-generation.log" 2>&1
fi
if test ! -f "$keys/container.pk8"; then
 openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out "$keys/container.pem" > "$keys/container-generation.log" 2>&1
 openssl req -new -x509 -key "$keys/container.pem" -out "$keys/container.x509.pem" -days 3650 -subj '/CN=TB371FC Local APEX com.android.runtime/'
 openssl pkcs8 -topk8 -nocrypt -in "$keys/container.pem" -outform DER -out "$keys/container.pk8"
fi
if test ! -e "$out/apex_payload.img"; then
 cp "$out/filesystem.img" "$out/apex_payload.img"
else
 cmp "$out/filesystem.img" "$out/apex_payload.img"
fi
"$avb" extract_public_key --key "$keys/payload.pem" --output "$out/apex_pubkey"
salt=$(sha256sum "$r/mounts/com.android.runtime/apex_manifest.pb" | cut -d' ' -f1)
max=$("$avb" add_hashtree_footer --partition_size 14929920 --calc_max_image_size --do_not_generate_fec --hash_algorithm sha256)
test "$max" -ge 14680064
"$avb" add_hashtree_footer --image "$out/apex_payload.img" --partition_size 14929920 --partition_name '' \
 --algorithm SHA256_RSA4096 --key "$keys/payload.pem" --salt "$salt" --hash_algorithm sha256 \
 --do_not_generate_fec --prop apex.key:com.android.runtime
"$avb" verify_image --image "$out/apex_payload.img" --key "$keys/payload.pem" > "$out/payload-verification.log" 2>&1
"$avb" info_image --image "$out/apex_payload.img" > "$out/payload-info.txt"
sha256sum "$out/apex_payload.img" "$out/apex_pubkey" > "$out/payload-SHA256SUMS"
echo EXT4_RUNTIME_AVB_SIGNATURE_AND_HASHTREE_PASS
