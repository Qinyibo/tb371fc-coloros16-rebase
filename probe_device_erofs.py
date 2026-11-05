import datetime,hashlib,ipaddress,json,pathlib,re,shlex,subprocess,sys
r=pathlib.Path(__file__).resolve().parent
target=sys.argv[1];ip,port=target.rsplit(':',1);ipaddress.ip_address(ip);assert 0<int(port)<65536
adb='C:/android-sdk/platform-tools/adb.exe';expected_boot='372004d3e4ad7985c58f9eade4961aa89a30ef8a5605e57e09eea0309e7129de'
suffix=sys.argv[2] if len(sys.argv)>2 else ''
assert suffix in ('','r2','r3')
out=r/('erofs-module-r107/device-trial'+('-'+suffix if suffix else ''));assert not out.exists();out.mkdir()
log=out/'commands.log'
def call(args,timeout=45):
 p=subprocess.run([adb,'-s',target,*args],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=timeout)
 with log.open('a',encoding='utf-8') as f:f.write(json.dumps(args)+'\n'+p.stdout+p.stderr+'\nRC='+str(p.returncode)+'\n')
 assert p.returncode==0,(args,p.returncode,p.stdout,p.stderr)
 return p.stdout.replace('\x00','')
def root(s,timeout=45):return call(['shell','su -c '+shlex.quote(s)],timeout)
pre=root('id; getprop ro.boot.serialno; sha256sum /dev/block/by-name/boot_a; cat /proc/sys/kernel/random/boot_id; pidof system_server com.android.systemui; cat /sys/fs/selinux/enforce')
assert 'uid=0(root)' in pre and 'REPLACE_WITH_DEVICE_SERIAL' in pre and expected_boot in pre,pre
boot_id=re.search(r'\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b',pre).group()
pid_lines=[l.strip() for l in pre.splitlines() if re.fullmatch(r'\d+(?: \d+)+',l.strip())];assert len(pid_lines)==1,pre
remote='/data/local/tmp/tb371fc-clean-rebase-erofs-20261104'+('-'+('r2' if suffix=='r3' else suffix) if suffix else '')
event=dict(timestamp=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),transport='wireless',endpoint=target,boot_id=boot_id,kind='Authorized EROFS component load/private read-only mount/unload trial; not a natural failure event or a ROM flash',existing_collector_unchanged=True)
(out/'event.json').write_text(json.dumps(event,indent=2))
assets={'device-probe':r/'erofs-module-r107/device-probe','erofs.ko':r/'erofs-module-r107/erofs.ko','runtime.img':r/'apex-inputs/com.android.runtime/apex_payload.img','expected.sha256':r/'erofs-module-r107/expected.sha256'}
expected={}
for n,p in assets.items():
 with p.open('rb') as f:expected[n]=hashlib.file_digest(f,'sha256').hexdigest()
assert expected['erofs.ko']==json.loads((r/'erofs-module-r107/build-result.json').read_text())['module_sha256']
if suffix!='r3':
 root(f'test ! -e {remote} && mkdir -m 0700 {remote} && chown 2000:2000 {remote}')
 for name,path in assets.items():call(['push',str(path),remote+'/'+name])
 root(f'chown 0:0 {remote} {remote}/* && chmod 0700 {remote} {remote}/device-probe && chmod 0600 {remote}/erofs.ko {remote}/runtime.img {remote}/expected.sha256')
hashes=root('sha256sum '+' '.join(remote+'/'+n for n in assets))
for name,digest in expected.items():assert digest+'  '+remote+'/'+name in hashes,hashes
# Factory APEX loop backing files carry system_file. The loop kernel thread
# cannot read a shell_data_file; use the real factory label on this one
# private test input rather than adding an allow or changing enforcement.
if suffix=='r3':
 label=root(f'chcon u:object_r:system_file:s0 {remote}/runtime.img && ls -lZ {remote}/runtime.img')
 assert 'u:object_r:system_file:s0' in label,label
# Native probe unshares mount namespace before loading the module, uses a
# private read-only/nosuid/nodev/noexec loop mount, then unmounts/unloads.
result=root(remote+'/device-probe '+remote,timeout=90)
(out/'probe-output.txt').write_text(result,encoding='utf-8')
assert all(marker in result for marker in ['NS_PRIVATE_OK','MODULE_LOADED','EROFS_MOUNTED_PRIVATE_READONLY','HASH_CHILD_STATUS=0','UNMOUNTED','LOOP_CLEARED','MODULE_UNLOADED','PROBE_RESULT=0']),result
checks=[l for l in result.splitlines() if l.endswith(': OK')];assert len(checks)==21,result
post=root('cat /proc/sys/kernel/random/boot_id; pidof system_server com.android.systemui; cat /sys/fs/selinux/enforce; grep "^erofs " /proc/modules || true')
assert boot_id in post and pid_lines[0] in post and 'erofs ' not in post and post.strip().endswith('1'),post
receipt=dict(scope='Actual r107 EROFS module load, isolated read-only original runtime image mount, 21 file SHA256 checks, and module unload; no Android runtime execution/APEX activation or new-ROM boot claim',timestamp=event['timestamp'],transport='wireless',device_boot_sha256=expected_boot,boot_id_unchanged=True,system_server_systemui_pids_unchanged=True,verified_runtime_files=21,module_loaded_and_unloaded=True,loop_cleared=True,root_mount_namespace_changed=False,existing_collector_unchanged=True,assets_sha256=expected,device_trial_pass=True)
(out/'result.json').write_text(json.dumps(receipt,indent=2));print('R107_EROFS_DEVICE_COMPONENT_PASS files=21 unloaded=true boot_and_core_pids_unchanged=true')
