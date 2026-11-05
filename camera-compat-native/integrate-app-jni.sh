#!/bin/bash
set -euo pipefail
r=/mnt/d/TB371FC-release/clean-rebase-20261104
w="$r/camera-compat-native/candidate-app-jni"
m="$w/mount-system"
base="$r/integrated-network/system-scale380-v4.img"
image="$r/integrated-network/system-camera-app-jni.img"
export TMPDIR="$r/temp" PYTHONDONTWRITEBYTECODE=1
mkdir -p "$w" "$m"
test ! -e "$image"
test "$(sha256sum "$base" | cut -d' ' -f1)" = e2e1f74deb320d817a3b5f5d90b31c5744f98f8eb6a8e98a0657719af59e4fd2
cp --reflink=auto --sparse=always "$base" "$image"
trap 'if mountpoint -q "$m"; then umount "$m"; fi' EXIT
mount -t ext4 -o loop,rw "$image" "$m"
python3 - "$r" "$w" "$m" <<'PY'
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys

root, work, mount = map(Path, sys.argv[1:])
donor = root / "mounts/my_product"
product = mount / "my_product"
app = product / "app/OplusCamera"
app_dir = app / "lib/arm64"
apk = "app/OplusCamera/OplusCamera.apk"

def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()

apk_hash = digest(donor / apk)
assert digest(product / apk) == apk_hash
assert not (app / "lib").exists()
context = os.getxattr(app, "security.selinux")
assert context == b"u:object_r:system_file:s0"
libraries = {
    "libCombineLutJni.so": "35472d1dcb09f6e09ee346f35eb07ca863b5fa2debf68f2be41bc44aaf9f880b",
    "libCombineLut.so": "793b4076808a9f18ced81c1fc962ae3efd6b015bf4d0dacf3b120dbf919d22b6",
}
for name, expected in libraries.items():
    assert digest(donor / "lib64" / name) == digest(product / "lib64" / name) == expected

# Match the OEM app-local JNI layout and keep the signed APK intact.
for directory in (app / "lib", app_dir):
    directory.mkdir(mode=0o755)
    os.chmod(directory, 0o755)
    os.chown(directory, 0, 0)
    os.setxattr(directory, "security.selinux", context)

dependencies = {}
for name, expected in libraries.items():
    target = app_dir / name
    shutil.copyfile(product / "lib64" / name, target)
    os.chmod(target, 0o644)
    os.chown(target, 0, 0)
    os.setxattr(target, "security.selinux", context)
    assert digest(target) == expected
    assert stat.S_IMODE(target.stat().st_mode) == 0o644 and target.stat().st_uid == target.stat().st_gid == 0
    assert os.getxattr(target, "security.selinux") == context
    header = subprocess.check_output(["readelf", "-h", str(target)], text=True)
    assert "AArch64" in header
    dynamic = subprocess.check_output(["readelf", "-d", str(target)], text=True)
    dependencies[name] = [line.split("[", 1)[1].split("]", 1)[0] for line in dynamic.splitlines() if "(NEEDED)" in line]

assert "libCombineLut.so" in dependencies["libCombineLutJni.so"]
assert "libCombineLutJni.so" not in dependencies["libCombineLut.so"]
assert digest(product / apk) == apk_hash
(work / "app-jni-integration.json").write_text(json.dumps({
    "donor": "OPD2413_16.0.10.600(CN01)",
    "target_dir": "/" + app_dir.relative_to(mount).as_posix(),
    "camera_apk_unchanged_sha256": apk_hash,
    "same_release_libraries_sha256": libraries,
    "needed": dependencies,
    "selinux_context": context.decode(),
    "scope": "App-local JNI files only. No APK changes, global linker grants, BSP changes or runtime mounts.",
}, indent=2) + "\n")
PY
umount "$m"
e2fsck -fn "$image" > "$w/system-fsck.log" 2>&1
printf '%s\n' CAMERA_APP_JNI_BUILD_FSCK_PASS
