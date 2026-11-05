#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/wifi-compat/apex"
mkdir -p "$w/source"
mount -t erofs -o ro,loop "$w/apex_payload.img" "$w/source"
find "$w/source/javalib" -maxdepth 1 -type f -printf '%f %s\n'
cp "$w/source/javalib/service-wifi.jar" "$w/service-wifi.original.jar"
