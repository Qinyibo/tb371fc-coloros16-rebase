"""Apply verified sparse RAW blocks to the current physical Fastboot super, without a wipe."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess

root = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument('--work', required=True)
parser.add_argument('--receipt', required=True)
parser.add_argument('--migrate-display-store', action='store_true')
parser.add_argument('--allow-camera-odm-config', action='store_true')
parser.add_argument('--allow-vendor-carrier-profile', action='store_true')
parser.add_argument('--allow-vendor-gpu-profile', action='store_true')
parser.add_argument('--allow-vendor-vnet', action='store_true')
args = parser.parse_args()
work = root / args.work
info = json.loads((work / 'delta-result.json').read_text(encoding='utf-8'))
candidate = json.loads((work / 'candidate.json').read_text(encoding='utf-8'))
current = json.loads((root / 'candidate-hwprofile-current.json').read_text(encoding='utf-8'))
receipt = json.loads((root / args.receipt).read_text(encoding='utf-8'))
serial = 'REPLACE_WITH_DEVICE_SERIAL'
assert receipt['serial'] == serial
assert receipt['boot_sha256'] == current['boot']['sha256'] == candidate['boot']['sha256']
assert receipt.get('expected_super_sha256', receipt.get('super_unchanged_sha256')) == current['super']['sha256'] == info['base_super_sha256']
assert candidate['super']['full_hash_verified'] and candidate['super']['sha256'] == info['updated_super_sha256']
allowed={'system_a', 'system_ext_a', 'product_a'}
if args.allow_camera_odm_config:
    proof_path = work / 'odm-config-integration.json'
    if proof_path.is_file():
        proof = json.loads(proof_path.read_text(encoding='utf-8'))
        profile = root / 'camera-compat-native/tb-camera-unit/camera_unit_config'
        assert proof['only_new_file'] == 'etc/camera/config/camera_unit_config'
        assert hashlib.sha256(profile.read_bytes()).hexdigest() == proof['file_sha256']
    else:
        proof = json.loads((root / 'camera-compat-native/odm-feature-integration.json').read_text(encoding='utf-8'))
        assert proof['only_new_file'] == 'etc/camera/config/camera_unit_feature_config.protobuf'
    assert proof['all_previous_bsp_entries_identical'] and proof['filesystem_check_pass']
    odm=info['partitions']['odm_a']
    assert odm['before_sha256']==proof['before_image_sha256']
    assert odm['sha256']==proof['after_image_sha256']
    allowed.add('odm_a')
if args.allow_vendor_carrier_profile:
    proof = json.loads((work / 'vendor-profile-integration.json').read_text(encoding='utf-8'))
    assert proof['only_changed_file'] == 'build.prop'
    assert proof['only_changed_property'] == 'ro.carrier'
    assert (proof['before_value'], proof['after_value']) == ('unknown', 'wifi-only')
    assert proof['all_other_entries_identical'] and proof['all_owners_modes_xattrs_symlinks_identical']
    assert proof['filesystem_check_pass'] and proof['entries_checked'] > 0
    vendor = info['partitions']['vendor_a']
    assert vendor['before_sha256'] == proof['before_image_sha256'] == current['logical_partitions']['vendor_a']['sha256']
    assert vendor['sha256'] == proof['after_image_sha256']
    allowed.add('vendor_a')
if args.allow_vendor_gpu_profile:
    proof = json.loads((work / 'gpu-profile-integration.json').read_text(encoding='utf-8'))
    policy = work / 'tb371fc-gpu-profile.rc'
    data = policy.read_bytes()
    assert proof['only_new_file'] == 'etc/init/tb371fc-gpu-profile.rc'
    assert proof['new_file_sha256'] == hashlib.sha256(data).hexdigest()
    assert proof['only_driver_parameter'] == '/sys/class/kgsl/kgsl-3d0/min_pwrlevel'
    assert proof['value'] == '4' and proof['board_guard'] == 'spinel'
    assert proof['boot_signal'] == 'vendor.post_boot.parsed=1'
    assert data.count(b'    write ') == 1
    assert data.endswith(b'    write /sys/class/kgsl/kgsl-3d0/min_pwrlevel 4\n')
    assert proof['all_previous_entries_identical'] and proof['entries_checked'] > 2000
    assert proof['filesystem_check_pass'] and proof['new_file_uses_existing_vendor_init_metadata']
    assert set(info['partitions']) == {'vendor_a'}
    vendor = info['partitions']['vendor_a']
    assert vendor['before_sha256'] == proof['before_image_sha256'] == current['logical_partitions']['vendor_a']['sha256']
    assert vendor['sha256'] == proof['after_image_sha256']
    allowed.add('vendor_a')
if args.allow_vendor_vnet:
    proof = json.loads((work / 'vnet-integration.json').read_text(encoding='utf-8'))
    assert set(proof['new_files']) == {'etc/init/tb371fc-vnet.rc', 'lib/modules/oplus_vnet.ko'}
    assert proof['all_previous_entries_identical'] and proof['entries_checked'] > 2000
    assert proof['filesystem_check_pass'] and proof['metadata_from_existing_vendor_files']
    ko = work.parent / 'vendor-overlay/lib/modules/oplus_vnet.ko'
    assert hashlib.sha256(ko.read_bytes()).hexdigest() == '01cb1335daddcf308d11076af1db50f5386c6bb94312243b02197d1a7bfc66bd'
    rc = (work.parent / 'vendor-overlay/etc/init/tb371fc-vnet.rc').read_text(encoding='utf-8')
    assert rc.count('    insmod ') == 1 and 'on post-fs-data && property:ro.product.board=spinel' in rc
    assert rc.rstrip().endswith('insmod /vendor/lib/modules/oplus_vnet.ko')
    vendor = info['partitions']['vendor_a']
    assert vendor['before_sha256'] == proof['before_image_sha256'] == current['logical_partitions']['vendor_a']['sha256']
    assert vendor['sha256'] == proof['after_image_sha256']
    allowed.add('vendor_a')
assert set(info['partitions']) <= allowed
assert info['partitions'] and info['parts']
bounds = [(p['start_sector'] * 512, p['start_sector'] * 512 + p['bytes']) for p in info['partitions'].values()]
parts = []
raw_bytes = 0
with (root / candidate['super']['path']).open('rb') as complete:
    for item in info['parts']:
        path = work / item['file']
        assert path.parent == work and path.stat().st_size == item['bytes'] <= 32 << 20
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == item['sha256']
        magic, major, minor, header, chunk, block, span, count, crc = struct.unpack_from('<IHHHHIIII', data)
        assert (magic, major, minor, header, chunk, block, span * block, crc) == (0xed26ff3a, 1, 0, 28, 12, 4096, info['bytes'], 0)
        offset, location = header, 0
        for _ in range(count):
            kind, pad, blocks, size = struct.unpack_from('<HHII', data, offset)
            length = blocks * block
            assert pad == 0 and length > 0
            if kind == 0xcac1:
                assert size == chunk + length and any(low <= location < location + length <= high for low, high in bounds)
                complete.seek(location)
                assert complete.read(length) == data[offset + chunk:offset + size]
                raw_bytes += length
            else:
                assert kind == 0xcac3 and size == chunk
            location += length
            offset += size
        assert location == info['bytes'] and offset == len(data)
        parts.append(path)
assert raw_bytes == info['changed_raw_bytes']
adb = ['D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe', '-P', '5037', '-s', serial]
fastboot = [str(root / 'flash-network-candidate/tools/fastboot.exe'), '-s', serial]
log = work / f'fastboot-{datetime.datetime.now():%Y%m%d-%H%M%S}.log'


def call(command, timeout=15):
    proc = subprocess.run(command, capture_output=True, timeout=timeout)
    message = (proc.stdout + proc.stderr).decode(errors='replace')
    with log.open('a', encoding='utf-8') as stream:
        stream.write(' '.join(map(str, command)) + '\n' + message + '\n')
    print(message.strip(), flush=True)
    assert proc.returncode == 0 and not re.search(r'\bFAILED\b|\berror:', message, re.I), command
    return message


assert call(adb + ['get-state']).strip() == 'device'
assert current['boot']['sha256'] in call(adb + ['shell', '/debug_ramdisk/su -c "sha256sum /dev/block/by-name/boot_a"'])
if args.migrate_display_store:
    migration_work = root / 'ui-compat/native-ui/display-store'
    migration = json.loads((migration_work / 'migration.json').read_text(encoding='utf-8'))
    assert migration['state'] == 'PREPARED_NOT_APPLIED' and migration['native_abx_decoder_verified']
    assert hashlib.sha256((migration_work / 'after.abx').read_bytes()).hexdigest() == migration['after_sha256']
    call(adb + ['push', str(migration_work / 'after.abx'), '/data/local/tmp/tb371fc-display-migration/after.abx'])
    call(adb + ['push', str(migration_work / 'migrate-before-fastboot.sh'), '/data/local/tmp/tb371fc-display-migration/migrate-before-fastboot.sh'])
    assert 'DISPLAY_STORE_TWO_FIELDS_MIGRATED_FRAMEWORK_STOPPED_FOR_FASTBOOT' in call(adb + ['shell', '/debug_ramdisk/su -c "sh /data/local/tmp/tb371fc-display-migration/migrate-before-fastboot.sh"'], timeout=20)
    migration['state'] = 'APPLIED_NEXT_BOOT_PENDING'
    (migration_work / 'migration.json').write_text(json.dumps(migration, indent=2) + '\n', encoding='utf-8')
call(adb + ['reboot', 'bootloader'])
for key, expected in {'is-userspace': 'no', 'product': 'spinel', 'unlocked': 'yes', 'current-slot': 'a',
                      'battery-soc-ok': 'yes', 'partition-size:super': '0x300000000'}.items():
    assert re.search(r'^' + re.escape(key) + r':\s*' + expected + r'\s*$',
                     call(fastboot + ['getvar', key], timeout=45), re.M | re.I), key
for path in parts:
    assert re.search(r"Writing 'super'.*OKAY", call(fastboot + ['flash', 'super', str(path)], timeout=45))
assert re.search(r'Rebooting.*OKAY', call(fastboot + ['reboot']))
result = dict(state='DELTA_WRITTEN_REBOOT_SENT_RUNTIME_PENDING', serial=serial, log=log.name,
              boot_sha256=current['boot']['sha256'], expected_super_sha256=info['updated_super_sha256'],
              userdata_wiped=False, partitions=list(info['partitions']), delta_parts=len(parts),
              physical_boot_verified=False)
result['display_store_two_field_migration_applied'] = args.migrate_display_store
(work / 'physical-delta-receipt.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
