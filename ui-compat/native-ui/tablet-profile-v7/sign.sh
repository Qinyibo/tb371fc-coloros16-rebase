#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/ui-compat/native-ui/tablet-profile-v7"
keys=/work/tb371fc-c16-network-prototype-20260930/keys
export TMPDIR="$r/temp" JAVA_TOOL_OPTIONS="-Djava.io.tmpdir=$r/temp -XX:-UsePerfData"
zipalign -f 4 "$w/unsigned.apk" "$w/aligned.apk"
apksigner sign --key "$keys/container.pk8" --cert "$keys/container.x509.pem" --min-sdk-version 34 --v1-signing-enabled false --v2-signing-enabled true --v3-signing-enabled true --v4-signing-enabled false --out "$w/LauncherResourceOverlay.apk" "$w/aligned.apk"
apksigner verify --min-sdk-version 34 --verbose --print-certs "$w/LauncherResourceOverlay.apk" > "$w/signature-verification.txt"
