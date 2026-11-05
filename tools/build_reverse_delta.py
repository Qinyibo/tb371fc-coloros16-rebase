"""Restore the old bytes for every RAW block in a verified forward delta."""

import argparse
import hashlib
import json
from pathlib import Path
import struct


SPARSE_HEADER = struct.Struct("<IHHHHIIII")
CHUNK = struct.Struct("<HHII")
BLOCK = 4096


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    work = (root / args.work).resolve()
    if not work.is_relative_to(root):
        parser.error("work must be inside the D: workspace")
    forward = json.loads((work / "delta-result.json").read_text(encoding="utf-8"))
    target = json.loads((work / "candidate.json").read_text(encoding="utf-8"))
    baseline = json.loads((root / forward["base_manifest"]).read_text(encoding="utf-8"))
    assert baseline["super"]["sha256"] == forward["base_super_sha256"]
    assert target["super"]["sha256"] == forward["updated_super_sha256"]
    assert forward["complete_image_readback_hash_verified"]
    reverse = work / "rollback-v2"
    reverse.mkdir(exist_ok=False)
    parts = []
    with (root / baseline["super"]["path"]).open("rb") as old, (root / target["super"]["path"]).open("rb") as new:
        for part in forward["parts"]:
            path = work / part["file"]
            raw = bytearray(path.read_bytes())
            assert len(raw) == part["bytes"] and hashlib.sha256(raw).hexdigest() == part["sha256"]
            magic, major, minor, header, chunk, block, span, count, crc = SPARSE_HEADER.unpack_from(raw)
            assert (magic, major, minor, header, chunk, block, crc) == (0xed26ff3a, 1, 0, 28, 12, BLOCK, 0)
            assert span * block == forward["bytes"]
            offset = header
            position = 0
            for _ in range(count):
                kind, pad, blocks, size = CHUNK.unpack_from(raw, offset)
                length = blocks * block
                assert pad == 0 and length > 0
                if kind == 0xcac1:
                    assert size == chunk + length
                    new.seek(position)
                    assert new.read(length) == raw[offset + chunk:offset + size]
                    old.seek(position)
                    original = old.read(length)
                    assert len(original) == length
                    raw[offset + chunk:offset + size] = original
                else:
                    assert kind == 0xcac3 and size == chunk
                offset += size
                position += length
            assert offset == len(raw) and position == forward["bytes"]
            (reverse / path.name).write_bytes(raw)
            parts.append({"file": path.name, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
    proof = {
        "use_only_when_super_is": target["super"]["sha256"],
        "restores_super_sha256": baseline["super"]["sha256"],
        "parts": parts,
        "userdata_wipe_required": False,
        "runtime_tested": False,
    }
    (reverse / "rollback.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(proof))


if __name__ == "__main__":
    main()
