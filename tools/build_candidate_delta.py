"""Build one complete candidate and bounded absolute sparse deltas from an exact base."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct

root = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument('--base', required=True)
parser.add_argument('--output', required=True)
parser.add_argument('--super-output', required=True)
parser.add_argument('--partition', action='append', required=True, help='logical_name=relative_image')
parser.add_argument('--scope', required=True)
args = parser.parse_args()
base = json.loads((root / args.base).read_text(encoding='utf-8'))
targets = dict(item.split('=', 1) for item in args.partition)
work = root / args.output
work.mkdir(exist_ok=True)
image = root / args.super_output
assert not image.exists() and not (work / 'delta-result.json').exists()
block = 4096
total = base['super']['bytes']
oldhash, newhash = hashlib.sha256(), hashlib.sha256()
runs, changes = [], {}

with (root / base['super']['path']).open('rb') as old, image.open('xb') as out:
    cursor = 0

    def unchanged(length):
        global cursor
        while length:
            data = old.read(min(length, 16 << 20))
            assert data
            oldhash.update(data)
            newhash.update(data)
            out.write(data)
            length -= len(data)
            cursor += len(data)

    for name in sorted(targets, key=lambda name: base['logical_partitions'][name]['start_sector']):
        previous = base['logical_partitions'][name]
        start, size = previous['start_sector'] * 512, previous['bytes']
        path = root / targets[name]
        assert path.stat().st_size == size and start % block == size % block == 0
        assert start >= cursor and start + size <= total
        unchanged(start - cursor)
        beforehash, afterhash = hashlib.sha256(), hashlib.sha256()
        changed = 0
        with path.open('rb') as new:
            for offset in range(0, size, 16 << 20):
                count = min(size - offset, 16 << 20)
                a, b = old.read(count), new.read(count)
                assert len(a) == len(b) == count
                oldhash.update(a)
                newhash.update(b)
                beforehash.update(a)
                afterhash.update(b)
                out.write(b)
                cursor += count
                if a == b:
                    continue
                for i in range(0, count, block):
                    payload = b[i:i + block]
                    if a[i:i + block] == payload:
                        continue
                    absolute = (start + offset + i) // block
                    changed += block
                    if runs and runs[-1][0] + len(runs[-1][1]) // block == absolute:
                        runs[-1][1].extend(payload)
                    else:
                        runs.append((absolute, bytearray(payload)))
            assert not new.read(1)
        assert beforehash.hexdigest() == previous['sha256'], name
        changes[name] = dict(path=targets[name], before_sha256=beforehash.hexdigest(),
                             sha256=afterhash.hexdigest(), bytes=size, start_sector=previous['start_sector'],
                             changed_bytes=changed)
    unchanged(total - cursor)
    assert not old.read(1)
    out.flush()
    os.fsync(out.fileno())
assert oldhash.hexdigest() == base['super']['sha256']
assert image.stat().st_size == total
assert hashlib.file_digest(image.open('rb'), 'sha256').hexdigest() == newhash.hexdigest()

header = struct.Struct('<IHHHHIIII')
chunk = struct.Struct('<HHII')
span = total // block
parts = []


def write(group):
    data, cursor, count = bytearray(), 0, 0
    for start, payload in group:
        if cursor < start:
            data.extend(chunk.pack(0xcac3, 0, start - cursor, 12))
            count += 1
        blocks = len(payload) // block
        data.extend(chunk.pack(0xcac1, 0, blocks, 12 + len(payload)))
        data.extend(payload)
        count += 1
        cursor = start + blocks
    if cursor < span:
        data.extend(chunk.pack(0xcac3, 0, span - cursor, 12))
        count += 1
    encoded = header.pack(0xed26ff3a, 1, 0, 28, 12, block, span, count, 0) + data
    assert len(encoded) <= 32 << 20
    path = work / f'super-delta-{len(parts):02d}.img'
    with path.open('xb') as stream:
        stream.write(encoded)
    parts.append(dict(file=path.name, bytes=len(encoded), sha256=hashlib.sha256(encoded).hexdigest()))


group, encoded = [], 40
for start, payload in runs:
    for offset in range(0, len(payload), 16 << 20):
        data = payload[offset:offset + (16 << 20)]
        extra = len(data) + 24
        if group and encoded + extra > 32 << 20:
            write(group)
            group, encoded = [], 40
        group.append((start + offset // block, data))
        encoded += extra
assert group
write(group)
result = dict(base_manifest=args.base, base_super_sha256=oldhash.hexdigest(),
              updated_super_sha256=newhash.hexdigest(), bytes=total, partitions=changes,
              parts=parts, changed_raw_bytes=sum(item['changed_bytes'] for item in changes.values()),
              scope=args.scope, complete_image_readback_hash_verified=True)
(work / 'delta-result.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
candidate = json.loads(json.dumps(base))
candidate.update(state='OFFLINE_BUILT_RUNTIME_PENDING', physical_tested=False,
                 delta=str((work / 'delta-result.json').relative_to(root)), scope=args.scope)
candidate['super'] = dict(path=args.super_output, sha256=newhash.hexdigest(), bytes=total, full_hash_verified=True)
for name, change in changes.items():
    candidate['logical_partitions'][name] = {k: change[k] for k in ('bytes', 'sha256', 'start_sector')}
for key in ('boot_id', 'system_server_pid'):
    candidate.pop(key, None)
(work / 'candidate.json').write_text(json.dumps(candidate, indent=2) + '\n', encoding='utf-8')
print('COMPLETE_IMAGE_AND_SPARSE_DELTA_VERIFIED', json.dumps(result), flush=True)
