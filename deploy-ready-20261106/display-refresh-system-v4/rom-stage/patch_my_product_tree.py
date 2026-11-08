#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib, shutil, sys
from pathlib import Path
EXPECTED = "35db38f8c85758c372546c707513642c"
HERE = Path(__file__).resolve().parent
SRC = HERE / "refresh_rate_config.xml"

def main():
    if len(sys.argv) != 2:
        print("usage: patch_my_product_tree.py <my_product_tree_root>")
        return 2
    root = Path(sys.argv[1])
    dst = root / "etc" / "refresh_rate_config.xml"
    if not (root / "etc").is_dir():
        print("ERROR: missing etc/ under", root)
        return 1
    data = SRC.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        print("ERROR: source has BOM")
        return 1
    h = hashlib.md5(data).hexdigest()
    if h != EXPECTED:
        print("ERROR: source MD5", h, "!=", EXPECTED)
        return 1
    shutil.copy2(SRC, dst)
    got = hashlib.md5(dst.read_bytes()).hexdigest()
    print("patched", dst)
    print("MD5", got)
    return 0 if got == EXPECTED else 1

if __name__ == "__main__":
    raise SystemExit(main())
