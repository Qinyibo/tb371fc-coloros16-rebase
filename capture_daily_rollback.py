import datetime, hashlib, json, os, pathlib, subprocess, sys
r=pathlib.Path(__file__).resolve().parent
adb=pathlib.Path('D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe')
out=r/'rollback-current-physical'
out.mkdir(exist_ok=False)
serial='REPLACE_WITH_DEVICE_SERIAL'
head=[str(adb),'-P','5037','-s',serial]
parts=[('boot_a',100663296),('vbmeta_a',65536),('vbmeta_system_a',65536),('super',12884901888)]
def capture(*args):
 return subprocess.check_output(head+list(args),timeout=15,text=True).strip()
start=capture('shell','cat /proc/sys/kernel/random/boot_id')
ota=capture('shell','getprop ro.build.version.ota')
slot=capture('shell','getprop ro.boot.slot_suffix')
assert slot=='_a' and ota.startswith('OPD2413_11.C.15_'), (slot,ota)
result={}
for n,size in parts:
 p=out/(n+'.img.partial')
 args=head+['exec-out',f"su -c 'dd if=/dev/block/by-name/{n} bs=1048576 status=none'"]
 h=hashlib.sha256(); total=0; report=1<<30
 with (out/(n+'.adb.log')).open('wb') as log, p.open('xb',buffering=0) as f, subprocess.Popen(args,stdout=subprocess.PIPE,stderr=log) as proc:
  try:
   while b:=proc.stdout.read(4<<20):
    total+=len(b)
    if total>size: raise RuntimeError((n,'source exceeds capacity',total))
    f.write(b);h.update(b)
    if total>=report:
     print(f'READ {n} {total>>30} GiB',flush=True);report+=1<<30
   if proc.wait(timeout=20)!=0 or total!=size:raise RuntimeError((n,proc.returncode,total,size))
   f.flush();os.fsync(f.fileno())
  except BaseException:
   if proc.poll() is None:proc.kill()
   raise
 final=p.with_suffix('')
 with p.open('rb') as f: check=hashlib.file_digest(f,'sha256').hexdigest()
 assert check==h.hexdigest(),n
 p.rename(final)
 result[n]=dict(path=final.name,bytes=size,sha256=check)
 print('ROLLBACK_READBACK_PASS',n,check,flush=True)
assert capture('shell','cat /proc/sys/kernel/random/boot_id')==start
assert capture('shell','getprop ro.boot.slot_suffix')==slot
assert result['boot_a']['sha256']=='372004d3e4ad7985c58f9eade4961aa89a30ef8a5605e57e09eea0309e7129de'
(out/'receipt.json').write_text(json.dumps(dict(scope='Exact running slot A static images read over USB; no userdata copied',serial=serial,slot=slot,boot_id=start,ota=ota,images=result),indent=2)+'\n')
print('CURRENT_DAILY_ROLLBACK_IMAGES_VERIFIED',flush=True)
