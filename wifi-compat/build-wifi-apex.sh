#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/wifi-compat";out="$w/rebuilt-wifi";keys="$r/private-signing/apex/com.android.wifi"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1 JAVA_TOOL_OPTIONS="-Djava.io.tmpdir=$r/temp -XX:-UsePerfData"
umask 077
mkdir -p "$keys"
if ! test -f "$keys/payload.pem"; then openssl genrsa -out "$keys/payload.pem" 4096; fi
umask 022
buildwork=/work/tb371fc-clean-wifi-20261105
mkdir -p "$buildwork"
mkdir "$out" "$buildwork/tree" "$out/check"
trap 'if mountpoint -q "$out/check"; then umount "$out/check"; fi' EXIT
rsync -aHAX --numeric-ids "$w/apex/source/" "$buildwork/tree/"
cp "$w/apex/service-wifi.compat.jar" "$buildwork/tree/javalib/service-wifi.jar"
# A profile tied to the original DEX checksum must not accompany changed code.
rm "$buildwork/tree/javalib/service-wifi.jar.prof"
python3 "$w/package-wifi-apex.py" audit "$r"
/root/aosp-tools/bin/mkfs.erofs -zlz4hc -C4096 -T0 -U d6e27762-67af-51dd-b470-5f1af236d487 "$out/apex_payload.img" "$buildwork/tree" > "$out/mkfs.log" 2>&1
mount -t erofs -o ro,loop "$out/apex_payload.img" "$out/check"
python3 "$r/verify_apex_tree.py" "$buildwork/tree" "$out/check" "$out" verify
umount "$out/check"
avb=/root/aosp-tools/bin/avbtool
"$avb" extract_public_key --key "$keys/payload.pem" --output "$out/apex_pubkey"
maxsize=$(( $(stat -c%s "$out/apex_payload.img") + 2*1024*1024 ))
salt=$(sha256sum "$w/apex/apex_manifest.pb" | cut -d' ' -f1)
"$avb" add_hashtree_footer --image "$out/apex_payload.img" --partition_size "$maxsize" --partition_name '' --algorithm SHA256_RSA4096 --hash_algorithm sha256 --key "$keys/payload.pem" --salt "$salt" --do_not_generate_fec --prop apex.key:com.android.wifi
"$avb" verify_image --image "$out/apex_payload.img" --key "$keys/payload.pem" > "$out/payload-verify.log" 2>&1
python3 "$w/package-wifi-apex.py" pack "$r"
zipalign -f 4096 "$out/unsigned.zip" "$out/aligned.apex"
container=/work/tb371fc-c16-network-prototype-20260930/keys
apksigner sign --key "$container/container.pk8" --cert "$container/container.x509.pem" --min-sdk-version 29 --v1-signing-enabled false --v2-signing-enabled true --v3-signing-enabled true --v4-signing-enabled false --out "$out/com.android.wifi.apex" "$out/aligned.apex"
apksigner verify --min-sdk-version 36 --verbose --print-certs "$out/com.android.wifi.apex" > "$out/container-verification.txt"
python3 "$w/package-wifi-apex.py" verify "$r"
