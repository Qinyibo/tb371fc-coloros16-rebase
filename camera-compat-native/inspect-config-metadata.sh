#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
file "$r/integrated-network/odm-camera-feature.img"
python3 - "$r/mounts/odm/etc/camera/config/camera_unit_feature_config.protobuf" <<'PY2'
from pathlib import Path
import os,sys
p=Path(sys.argv[1]);s=p.stat();print('DONOR_CONFIG_META',oct(s.st_mode),s.st_uid,s.st_gid,{k:os.getxattr(p,k).decode(errors='replace') for k in os.listxattr(p)})
PY2
