#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
a="$r/mounts/odm/etc/camera/config"
for name in camera_unit_config camera_unit_feature_config.protobuf oplus_camera_config; do
  file "$a/$name"
  sha256sum "$a/$name"
  od -An -t x1 -N 40 "$a/$name"
done
cmp -l "$a/camera_unit_config" "$a/camera_unit_feature_config.protobuf" | head -12 || true
