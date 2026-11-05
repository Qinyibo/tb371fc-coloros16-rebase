"""Build the TB foreground service against the verified .600 platform ABI."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compiler", required=True, type=Path)
    parser.add_argument("--output", default="build", type=Path)
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    output = (root / args.output).resolve()
    if not output.is_relative_to(root):
        parser.error("output must be inside scheduler-compat on D:")
    output.mkdir(parents=True, exist_ok=True)

    framework = root / "power/framework.jar"
    binder = root / "power/libbinder_ndk.so"
    if digest(framework) != "2ca0ce08927974f277cc15f85a33e5f0ac9c9491996a19955f8b2273a987d30d":
        raise RuntimeError("Expected the .600 framework used to derive the power transaction")
    if digest(binder) != "0ef7b4a9844df4084f4b4e87a661224b4ca3de7d527a109a893c328aae03f100":
        raise RuntimeError("Unexpected platform Binder library")
    stub, = (root / "power/framework-context").rglob("IPowerManager$Stub.smali")
    if not re.search(r"TRANSACTION_isInteractive:I = 0x15\b", stub.read_text(encoding="utf-8")):
        raise RuntimeError("Unexpected power transaction code")

    targets = {"tb371fc-scheduler": "src/runtime.c", "selector-read-only": "tests/selector.c"}
    built = {}
    for name, source in targets.items():
        binary = output / name
        build = subprocess.run(
            [str(args.compiler.resolve()), "-O2", "-Wall", "-Wextra", "-Werror",
             "-Wno-misleading-indentation", "-fstack-protector-strong", "-D_FORTIFY_SOURCE=2",
             "-fPIE", "-pie", "-Wl,-z,relro,-z,now", str(root / source),
             str(root / "src/power.c"), str(binder), "-o", str(binary)],
            capture_output=True, timeout=90, cwd=root,
        )
        (output / (name + "-compile.log")).write_bytes(build.stdout + build.stderr)
        build.check_returncode()
        contents = binary.read_bytes()
        if not contents.startswith(b"\x7fELF") or any(
            marker in contents for marker in (b"/data/adb", b"busybox", b"/sys/class/drm")
        ):
            raise RuntimeError(f"Unexpected dependency in {name}")
        built[name] = {"sha256": digest(binary), "bytes": len(contents)}
    (output / "rebuild.json").write_text(json.dumps(built, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(built))


if __name__ == "__main__":
    main()
