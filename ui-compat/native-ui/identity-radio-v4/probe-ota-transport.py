"""Bounded capture of the native updater's DNS requests; no UI/settings changes."""
import json, shlex, subprocess, time
from pathlib import Path

out = Path('ui-compat/native-ui/identity-radio-v4/ota-transport-v4')
out.mkdir(exist_ok=False)
adb = ['D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe', '-P', '5037', '-s', 'REPLACE_WITH_DEVICE_SERIAL']

def command(text):
    return adb + ['shell', '/debug_ramdisk/su -c ' + shlex.quote(text)]

def run(text):
    result = subprocess.run(command(text), capture_output=True, timeout=25)
    assert result.returncode == 0, (text, result.stderr)
    return result.stdout.decode(errors='replace').replace('\r', '')

query = "content query --uri content://com.oplus.customize.coreapp.configmanager.configprovider.AppFeatureProvider/app_feature --where \"featurename='com.oplus.ota.component_update_url'\""
(out / 'active-endpoint.txt').write_text(run(query), encoding='utf-8')
(out / 'before.txt').write_text(run('cat /proc/sys/kernel/random/boot_id; pidof com.android.phone; settings get system oplus_customize_ota_patch; content query --uri content://com.oplus.ota/pkgList'), encoding='utf-8')
with (out / 'dns.txt').open('wb') as dns, (out / 'tcpdump-stderr.txt').open('wb') as errors:
    capture = subprocess.Popen(command("timeout -s INT 15 /system/bin/tcpdump -i any -nn -vv -l 'udp port 53 or tcp port 53'"), stdout=dns, stderr=errors)
    time.sleep(2)
    assert capture.poll() is None, 'Capture did not start'
    action = run('am broadcast -a oplus.intent.ota.OTA_CHECK_NEW_VERSION_UPDATE -n com.oplus.ota/com.oplus.ota.strategy.StrategyReceiver --es query_update_mode manual')
    (out / 'manual-action.txt').write_text(action, encoding='utf-8')
    result = capture.wait(timeout=22)
(out / 'after.txt').write_text(run('cat /proc/sys/kernel/random/boot_id; pidof com.android.phone; settings get system oplus_customize_ota_patch; content query --uri content://com.oplus.ota/pkgList'), encoding='utf-8')
packets = (out / 'dns.txt').read_text(errors='replace')
result = {'capture_exit_code': result, 'pinned_domain_observed': 'updates.tb371fc.invalid' in packets, 'dns_lines': len(packets.splitlines())}
(out / 'result.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result))
