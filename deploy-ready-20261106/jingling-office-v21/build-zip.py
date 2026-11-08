#!/usr/bin/env python3
# Build Magisk zip with forward-slash entry names only (Windows zip tools break Magisk).
import hashlib, os, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MOD = ROOT / "magisk-module"
OUT = ROOT / "tb371fc_jingling_office_v21.zip"

def add_tree(zf: zipfile.ZipFile, base: Path):
    for path in sorted(base.rglob("*")):
        if path.is_dir():
            continue
        rel = path.relative_to(base).as_posix()  # forward slashes
        # Magisk: compress metadata; store huge apk to speed install
        compress = zipfile.ZIP_STORED if path.suffix.lower() == ".apk" else zipfile.ZIP_DEFLATED
        zf.write(path, rel, compress_type=compress)
        print(f" + {rel} ({path.stat().st_size}) compress={compress}")

if OUT.exists():
    OUT.unlink()

with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
    add_tree(zf, MOD)

h = hashlib.sha256()
with open(OUT, "rb") as f:
    for chunk in iter(lambda: f.read(1024 * 1024), b""):
        h.update(chunk)
print(f"OUT={OUT}")
print(f"SIZE={OUT.stat().st_size}")
print(f"SHA256={h.hexdigest().upper()}")