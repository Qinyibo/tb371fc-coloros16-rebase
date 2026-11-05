import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parent.parent
work = root/'wifi-compat'
packet = root/'flash-network-candidate'
serial = 'REPLACE_WITH_DEVICE_SERIAL'
fastboot = str(packet/'tools/fastboot.exe')
result = json.loads((work/'delta-result.json').read_text(encoding='utf-8'))
qspm=json.loads((root/'qspm-compat/delta-result.json').read_text(encoding='utf-8'))
prior=json.loads((root/'qspm-compat/physical-delta-receipt.json').read_text(encoding='utf-8'))
boot=json.loads((work/'physical-flash-receipt.json').read_text(encoding='utf-8'))
assert qspm['updated_super_sha256']==result['base_super_sha256'] and prior['serial']==serial and prior['state']=='PATCH_WRITTEN_AND_CLEAN_REBOOT_REQUESTED'
assert boot['boot_sha256']=='dfad1ca0f466b205fccdb28271188538fce7ced9fd099fd01e9358dc61613db8' and boot['changed_partitions']==['boot_a']
parts=[]
for number, part in enumerate(result['parts']):
    path=work/f'super-wifi-delta-{number:02d}.img'
    assert part['file']==path.name and part['bytes']==path.stat().st_size<=32<<20
    assert hashlib.sha256(path.read_bytes()).hexdigest()==part['sha256']
    parts.append(path)
assert parts
log=work/f'fastboot-wifi-{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}.log'

def call(*args, timeout=12):
    command=[fastboot,'-s',serial,*map(str,args)]
    p=subprocess.run(command,capture_output=True,timeout=timeout)
    message=(p.stdout+p.stderr).decode(errors='replace')
    with log.open('a',encoding='utf-8') as f:
        f.write(' '.join(map(str,args))+'\n'+message+'\n')
    print(message.strip(),flush=True)
    if p.returncode or re.search(r'\bFAILED\b|\berror:',message,re.I):
        raise RuntimeError(args)
    return message

for key,value in {'is-userspace':'no','product':'spinel','unlocked':'yes','current-slot':'a','battery-soc-ok':'yes','partition-size:super':'0x300000000','partition-size:metadata':'0x1000000'}.items():
    assert re.search(r'^'+re.escape(key)+r':\s*'+value+r'\s*$',call('getvar',key),re.M|re.I),key
for part in parts:
    assert re.search(r"Writing 'super'.*OKAY",call('flash','super',part,timeout=35))
assert re.search(r"Setting current slot to 'a'.*OKAY",call('set_active','a'))
assert re.search(r'^slot-unbootable:a:\s*no\s*$',call('getvar','slot-unbootable:a'),re.M)
assert re.search(r'Rebooting.*OKAY',call('reboot'))
(work/'physical-delta-receipt.json').write_text(json.dumps(dict(state='WIFI_PATCH_WRITTEN_REBOOT_SENT_RUNTIME_PENDING',userdata_wiped=False,boot_sha256=boot['boot_sha256'],expected_super_sha256=result['updated_super_sha256'],serial=serial,log=log.name,delta_parts=len(parts),device_boot_completed=False),indent=2)+'\n',encoding='ascii')
