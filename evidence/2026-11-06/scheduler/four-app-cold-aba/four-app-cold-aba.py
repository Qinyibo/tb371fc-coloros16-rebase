from pathlib import Path
import datetime, json, re, shlex, subprocess, time

root = Path.cwd()
work = root / 'scheduler-compat/resume-20261106' / ('four-app-cold-aba-' + datetime.datetime.now().strftime('%H%M%S'))
work.mkdir(parents=True)
adb = ['D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe', '-P', '5037', '-s', 'REPLACE_WITH_DEVICE_SERIAL']
apps = ['com.ss.android.ugc.aweme', 'com.tencent.mm', 'com.tencent.mobileqq', 'com.luna.music']
service = 'tb371fc-scheduler'
group = '/dev/tb371fc-schedtune/foreground'
boot = '/proc/sys/kernel/random/boot_id'
remote = '/data/local/tmp/tb371fc-four-app-' + work.name[-6:]


def shell(command, timeout=20):
    result = subprocess.run(adb + ['shell', '/debug_ramdisk/su -c ' + shlex.quote(command)], capture_output=True, timeout=timeout, check=True)
    return result.stdout.decode('utf-8', errors='replace').replace('\r', '')


def state():
    command = f'getprop init.svc.{service}; cat {group}/schedtune.boost {group}/schedtune.prefer_idle; wc -l < {group}/tasks'
    values = shell(command).split()
    if len(values) != 4:
        raise RuntimeError(f'Invalid scheduler state: {values}')
    return values


def await_state(enabled):
    until = time.monotonic() + 12
    while time.monotonic() < until:
        values = state()
        if enabled and values[:3] == ['running', '30', '1'] and int(values[3]) > 0:
            return values
        if not enabled and values == ['stopped', '0', '0', '0']:
            return values
        time.sleep(.3)
    raise RuntimeError(f'Scheduler transition incomplete: {values}')


def withdraw():
    pid = shell(f'getprop init.svc_debug_pid.{service}').strip()
    assert pid.isdecimal() and int(pid) > 1
    assert shell(f'readlink /proc/{pid}/exe').strip() == '/system_ext/bin/tb371fc-scheduler'
    shell(f'kill -TERM {pid}')
    return await_state(False)


def ensure_unlocked(home=False):
    assert 'secure=false' in shell('dumpsys window policy | grep -m1 secure=')
    shell('input keyevent KEYCODE_WAKEUP; wm dismiss-keyguard' + ('; input keyevent KEYCODE_HOME' if home else ''))
    until = time.monotonic() + 8
    while time.monotonic() < until:
        if 'mWakefulness=Awake' in shell('dumpsys power | grep -m1 mWakefulness=') and 'showing=false' in shell('dumpsys window policy | grep -m1 showing='):
            return
        time.sleep(.25)
    raise RuntimeError('Tablet did not reach unlocked interactive state')


def restore():
    if state()[0] != 'running':
        shell(f'setprop ctl.start {service}')
    if 'mWakefulness=Asleep' in shell('dumpsys power | grep -m1 mWakefulness='):
        values=state()
        if values==['running','0','0','0']:
            return values
    return await_state(True)


invariants = 'cat ' + boot + '; cat /sys/class/kgsl/kgsl-3d0/min_pwrlevel; getprop init.svc.tb371fc-speaker; getenforce'
assert shell('sha256sum /system_ext/bin/tb371fc-scheduler').split()[0] == '76995e3ce9469a605ed0f07c23d9e3c1f92582f026107202d4ff76941d810c07'
initial = state()
assert initial[0] == 'running', initial
baseline = shell(invariants).splitlines()
assert baseline[1:] == ['4', 'running', 'Enforcing'], baseline
power = shell('dumpsys power | grep -m1 mWakefulness=')
was_asleep = 'Asleep' in power
ensure_unlocked(home=True)
await_state(True)
resolution = shell('dumpsys window displays | grep -m1 mDisplayRotation')
width, height = map(int, re.search(r'mBounds=Rect\(0, 0 - (\d+), (\d+)\)', resolution).groups())
rotation = re.search(r'mDisplayRotation=ROTATION_\d+',resolution)[0]
components = {app:shell(f'cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -p {app}').strip().splitlines()[-1] for app in apps}
assert all(c.startswith(a+'/') for a,c in components.items())
work.joinpath('plan.json').write_text(json.dumps({'apps':components,'rotation':rotation,'width':width,'height':height,'warmup_full_cycles':1,'measured_cycles':2,'baseline':baseline,'initial_scheduler':initial,'subjective_capture':False},indent=2)+'\n')
print('OUTPUT',work,flush=True)

config = Path(__file__).with_name('compact-trace.pbtxt').read_text(encoding='utf-8').replace('duration_ms: 15000','duration_ms: 63000').replace('tb371fc-compact-repro-20261105', work.name)
config = config.replace(' atrace_categories: "gfx"',' ftrace_events: "sched/sched_process_exit"\n ftrace_events: "task/task_newtask"\n ftrace_events: "task/task_rename"\n atrace_categories: "gfx"')
config = config.replace(' atrace_apps: "com.android.systemui"',' atrace_apps: "com.android.systemui"\n' + '\n'.join(f' atrace_apps: "{app}"' for app in apps))
config_path = work/'config.pbtxt'; config_path.write_text(config,encoding='utf-8',newline='\n')
subprocess.run(adb+['push',str(config_path),remote+'.pbtxt'],check=True,timeout=15,capture_output=True)


def workload():
    # Keep the previous app foregrounded when stopping and launching the next target.
    x=width//2; low=int(height*.73); high=int(height*.34)
    sample = (f'printf "STATE "; getprop init.svc.{service}; '
              f'printf "TUNE "; tr "\\n" " " < {group}/schedtune.boost; tr "\\n" " " < {group}/schedtune.prefer_idle; wc -l < {group}/tasks; '
              'printf "THERMAL "; for z in 0 1 5; do tr "\\n" " " < /sys/class/thermal/thermal_zone$z/temp; done; echo; '
              'dumpsys battery | grep "temperature:"; dumpsys display | grep -m1 mActiveSfDisplayMode; '
              'dumpsys window | grep -m1 mCurrentFocus')
    blocks=['echo WINDOW_BEGIN $(cat /proc/uptime)']
    for cycle in range(2):
        for app, component in components.items():
            blocks.extend([f'echo APP {cycle+1} {app}', f'am force-stop --user 0 {app}',
              f'if pidof {app} >/dev/null; then echo COLD_GATE_FAILED {app}; exit 21; fi',
              'echo LAUNCH_BEGIN $(cat /proc/uptime)',
              f'timeout 8 am start -W --user 0 --windowingMode 1 -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -n {shlex.quote(component)} || echo LAUNCH_FAILED {app}',
              'echo SWIPE_BEGIN $(cat /proc/uptime)',
              f'input swipe {x} {low} {x} {high} 320; sleep 0.25; input swipe {x} {low} {x} {high} 320; sleep 0.28',
              sample, 'echo APP_END $(cat /proc/uptime)'])
    blocks.append('echo WINDOW_END $(cat /proc/uptime)')
    return '\n'.join(blocks)


full = workload()
first_pass, _ = full.split('echo APP 2 ', 1)
warm = first_pass+'echo WINDOW_END $(cat /proc/uptime)'
work.joinpath('workload.sh').write_text(full+'\n',encoding='utf-8',newline='\n')


def run_phase(label, enabled):
    folder = work/label; folder.mkdir()
    ensure_unlocked(home=True)
    assert await_state(enabled)
    print('WARMUP',label,state(),flush=True)
    warm_data=shell(warm,timeout=48)
    folder.joinpath('warmup.txt').write_text(warm_data,encoding='utf-8')
    assert 'NotificationShade' not in warm_data and warm_data.count('LaunchState: COLD')==4, 'Warmup is not a valid four-app cold cycle'
    assert 'showing=false' in shell('dumpsys window policy | grep -m1 showing=')
    assert shell(invariants).splitlines() == baseline
    assert await_state(enabled)
    result = folder/'workload.txt'
    output = remote+'-'+label+'.pftrace'
    capture = None
    try:
        with (folder/'capture.log').open('wb') as log:
            capture = subprocess.Popen(adb+['shell','/debug_ramdisk/su -c '+shlex.quote(f'perfetto --txt -c {remote}.pbtxt -o {output}')],stdout=log,stderr=subprocess.STDOUT)
            until = time.monotonic()+9
            while b'Connected to the Perfetto' not in (folder/'capture.log').read_bytes():
                assert capture.poll() is None and time.monotonic()<until, 'Perfetto did not start'
                time.sleep(.2)
            print('MEASURING',label,flush=True)
            measured=shell(full,timeout=57)
            result.write_text(measured,encoding='utf-8')
            assert 'NotificationShade' not in measured and 'showing=false' in shell('dumpsys window policy | grep -m1 showing='), 'Keyguard interrupted measurement'
            assert shell(invariants).splitlines() == baseline
            folder.joinpath('end-state.json').write_text(json.dumps(state())+'\n')
            if not enabled:
                # Workload is finished. Restore while the trace closes and is copied.
                print('RESTORED_AFTER_B',restore(),flush=True)
            assert capture.wait(timeout=70)==0
        with (folder/'heavy.pftrace').open('wb') as file:
            subprocess.run(adb+['exec-out','/debug_ramdisk/su -c '+shlex.quote('cat '+output)],stdout=file,stderr=subprocess.PIPE,check=True,timeout=45)
        assert (folder/'heavy.pftrace').stat().st_size > 100000
        folder.joinpath('events.txt').write_text(shell('logcat -b events -d -v monotonic | grep -E "am_(proc_died|crash|anr|kill|proc_start)" | tail -350'),encoding='utf-8')
        print('PHASE_COMPLETE',label,flush=True)
    finally:
        if not enabled and state()[0]!='running':
            print('RESTORE_ON_EXIT',restore(),flush=True)
        if capture and capture.poll() is None:
            try:
                capture.wait(timeout=66)
            except subprocess.TimeoutExpired:
                capture.terminate()
                capture.wait(timeout=5)
        shell('rm -f '+output)


try:
    run_phase('A1',True)
    ensure_unlocked()
    print('B_WITHDRAWN',withdraw(),flush=True)
    run_phase('B',False)
    run_phase('A2',True)
finally:
    ensure_unlocked()
    restored = restore()
    if was_asleep:
        shell('input keyevent KEYCODE_SLEEP')
    shell('rm -f '+remote+'.pbtxt')
    final = state()
    assert final[0]=='running' and shell(invariants).splitlines()==baseline
    work.joinpath('restoration.json').write_text(json.dumps({'restored_awake_state':restored,'final':final,'original_sleep_restored':was_asleep,'permanent_changes':False},indent=2)+'\n')
    print('FINAL_STATE',final,flush=True)
