import datetime,hashlib,json,re,subprocess
from pathlib import Path
r=Path(__file__).resolve().parent.parent;w=r/'wifi-compat';info=json.loads((w/'boot/result.json').read_text());img=w/'boot/boot-a-OFFLINE.img'
assert img.stat().st_size==100663296 and hashlib.sha256(img.read_bytes()).hexdigest()==info['sha256']=='dfad1ca0f466b205fccdb28271188538fce7ced9fd099fd01e9358dc61613db8'
abi=json.loads((w/'kernel-build/abi-verification.json').read_text());assert abi['original_exports']==13081 and not abi['removed'] and not abi['changed'] and len(abi['modules'])==9 and not any(x['nonmatching'] for x in abi['modules'])
fb=str(r/'flash-network-candidate/tools/fastboot.exe');serial='REPLACE_WITH_DEVICE_SERIAL';log=w/('flash-correct-bsp-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'.log')
def call(*args,timeout=12):
 p=subprocess.run([fb,'-s',serial,*map(str,args)],capture_output=True,timeout=timeout);t=(p.stdout+p.stderr).decode(errors='replace');print(t.strip(),flush=True)
 with log.open('a',encoding='utf-8') as f:f.write(' '.join(map(str,args))+'\n'+t+'\n')
 assert p.returncode==0 and not re.search(r'\bFAILED\b|\berror:',t,re.I),args
 return t
for k,v in {'is-userspace':'no','product':'spinel','unlocked':'yes','current-slot':'a','battery-soc-ok':'yes','partition-size:boot_a':'0x6000000'}.items():
 assert re.search(r'^'+re.escape(k)+r':\s*'+v+r'\s*$',call('getvar',k),re.M|re.I),k
assert re.search(r"Writing 'boot_a'.*OKAY",call('flash','boot_a',img,timeout=45))
assert re.search(r'Rebooting.*OKAY',call('reboot'))
(w/'physical-flash-receipt.json').write_text(json.dumps({'state':'BOOT_WRITTEN_REBOOT_SENT_RUNTIME_PENDING','serial':serial,'boot_sha256':info['sha256'],'changed_partitions':['boot_a'],'userdata_wiped':False,'log':log.name},indent=2)+'\n')
