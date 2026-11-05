import argparse
import hashlib
import json
import pathlib
import re
import socket
import subprocess

root = pathlib.Path(__file__).resolve().parent
adb = pathlib.Path('D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe')
parser = argparse.ArgumentParser(description='One read-only device snapshot for TB371FC clean rebase acceptance')
parser.add_argument('tag', choices=['daily', 'clean-first-boot'])
args = parser.parse_args()
with socket.create_connection(('127.0.0.1', 5037), timeout=2):
    pass
head = [str(adb), '-P', '5037', '-s', 'REPLACE_WITH_DEVICE_SERIAL', 'shell']

def shell(command, timeout=12):
    p = subprocess.run(head+[command], timeout=timeout, capture_output=True)
    return dict(status=p.returncode, output=p.stdout.decode(errors='replace').replace('\r\n','\n'), error=p.stderr.decode(errors='replace'))

queries = {
    'identity': 'getprop ro.build.version.ota; getprop ro.build.version.sdk; getprop ro.boot.slot_suffix; getprop sys.boot_completed; cat /proc/sys/kernel/random/boot_id; uname -r; getenforce',
    'mounts': '''grep -E ' /apex/com.android.(runtime|tethering)(@| )' /proc/mounts''',
    'network_loader': 'getprop init.svc.mdnsd_netbpfload; getprop init.svc.bpfloader; getprop bpf.progs_loaded; getprop init.svc.netd; service check connectivity; service check wifi',
    'cameras': '''pm path com.oplus.camera; pm path com.zui.camera; service check media.camera; dumpsys media.camera | grep -Ei '^Number of (normal )?camera devices|Camera Provider HAL|^== Camera device [0-9] dynamic' ''',
    'display': 'wm size; wm density; settings get system peak_refresh_rate; settings get system min_refresh_rate; settings get global window_animation_scale; settings get global transition_animation_scale; settings get global animator_duration_scale',
    'launcher': 'cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.HOME',
}
results = {k:shell(v) for k,v in queries.items()}
expected = 'OPD2413_11.C.15_' if args.tag=='daily' else 'OPD2413_11.C.35_'
lines = results['identity']['output'].splitlines()
assert results['identity']['status']==0 and len(lines)>=7 and lines[0].startswith(expected), results['identity']
assert lines[1:4]==['36','_a','1'] and lines[-1]=='Enforcing', lines
launcher_lines = results['launcher']['output'].splitlines()
home = launcher_lines[-1].partition('/')[0] if launcher_lines else ''
if re.fullmatch(r'[a-zA-Z0-9_.]+', home):
    results['launcher_stats'] = shell(f'''dumpsys gfxinfo {home} | grep -E 'Total frames rendered|Janky frames|percentile|Missed Vsync' ''')
raw = dict(scope='Boot and service registration snapshot only; no camera capture, network traffic or performance claim', results=results)
path = root / ('device-acceptance-'+args.tag+'.json')
with path.open('x',encoding='utf-8') as f:
    json.dump(raw,f,ensure_ascii=False,indent=2)
    f.write('\n')
print(path.name)
for key in ('identity','network_loader','cameras'):
    print(key, results[key]['output'])
