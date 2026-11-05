#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
src="$r/mounts/odm/etc/camera/config/camera_unit_feature_config.protobuf"
mountpoint -q "$r/mounts/odm"
test -f "$src"
mkdir -p "$r/camera-compat-native/config-donor"
cp "$src" "$r/camera-compat-native/config-donor/camera_unit_feature_config.protobuf"
sha256sum "$src" "$r/camera-compat-native/config-donor/camera_unit_feature_config.protobuf"
