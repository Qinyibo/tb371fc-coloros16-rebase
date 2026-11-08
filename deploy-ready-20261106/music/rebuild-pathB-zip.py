import os, zipfile, hashlib, shutil
from pathlib import Path

base = Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\music")
mod = base / "magisk-module-luna-heap-offset"
so_src = base / "libsysoptimizer.so.patched-disable-apply"
so_dst = mod / "lib" / "libsysoptimizer.so"

mod.joinpath("lib").mkdir(parents=True, exist_ok=True)
shutil.copy2(so_src, so_dst)
h = hashlib.sha256(so_dst.read_bytes()).hexdigest()
print("tree_so_sha", h)
assert h == "2dc3bda37442e36f9fd6d3b2a19aec427e59c0393449f0ffb433095c94cf0b4e"

pfs = (mod / "post-fs-data.sh").read_text(encoding="utf-8")
assert "PATHB=2dc3bda37442e36f9fd6d3b2a19aec427e59c0393449f0ffb433095c94cf0b4e" in pfs
assert "lib/libsysoptimizer.so" in pfs
assert "ORIG=" in pfs and "PATHA=" in pfs

upd_bin = mod / "META-INF" / "com" / "google" / "android" / "update-binary"
upd_scr = mod / "META-INF" / "com" / "google" / "android" / "updater-script"
print("update-binary size", upd_bin.stat().st_size if upd_bin.exists() else None)
print("updater-script", (upd_scr.read_text(encoding="utf-8") if upd_scr.exists() else None))

out = base / "tb371fc_luna_heap_offset_fix-v1-pathB-fixed.zip"
if out.exists():
    out.unlink()

include = []
for root, dirs, files in os.walk(mod):
    for fn in files:
        full = Path(root) / fn
        rel = full.relative_to(mod).as_posix()
        include.append((full, rel))

with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for full, rel in sorted(include, key=lambda x: x[1]):
        zi = zipfile.ZipInfo(filename=rel)
        zi.compress_type = zipfile.ZIP_DEFLATED
        data = full.read_bytes()
        if rel.endswith(".sh") or rel.endswith("update-binary"):
            zi.external_attr = (0o755 << 16)
        else:
            zi.external_attr = (0o644 << 16)
        zf.writestr(zi, data)
        print("added", rel, len(data))

with zipfile.ZipFile(out, "r") as zf:
    names = zf.namelist()
    print("ZIP_NAMES:")
    for n in names:
        print(" ", n)
        if "\\" in n:
            raise SystemExit("backslash in zip entry: " + n)
    data = zf.read("lib/libsysoptimizer.so")
    print("zip_so_sha", hashlib.sha256(data).hexdigest())
print("OUT", out, out.stat().st_size)