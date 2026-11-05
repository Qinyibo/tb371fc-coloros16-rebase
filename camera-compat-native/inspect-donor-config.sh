#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
file "$r/donor-images/odm.img"
if mountpoint -q "$r/mounts/odm"; then
 findmnt -n -o SOURCE,FSTYPE,OPTIONS --target "$r/mounts/odm"
 ls -l "$r/mounts/odm/etc/camera/config/oplus_camera_feature_config" "$r/mounts/odm/etc/camera/config/camera_unit_feature_config.protobuf" 2>/dev/null || true
fi
