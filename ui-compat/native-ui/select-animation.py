"""Exercise the actual Settings preference and its explicit reboot button."""
import argparse
from pathlib import Path
import re
import subprocess
import time
import xml.etree.ElementTree as ET

root=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--mode',choices=['2','4'],required=True)
parser.add_argument('--output',required=True)
args=parser.parse_args()
work=(root/args.output).resolve();assert work.is_relative_to(root);work.mkdir(parents=True,exist_ok=True)
adb=['D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe','-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL']
commands=[]

def shell(command):
    proc=subprocess.run(adb+['shell',command],capture_output=True,timeout=25)
    message=(proc.stdout+proc.stderr).decode(errors='replace').replace('\r','')
    commands.append(command+'\n'+message)
    assert proc.returncode==0,(command,message[-600:])
    return message

def dump(name):
    shell('uiautomator dump /data/local/tmp/tb371fc-animation-validation.xml')
    data=shell('cat /data/local/tmp/tb371fc-animation-validation.xml')
    (work/name).write_text(data,encoding='utf-8')
    return ET.fromstring(data)

def tap(tree,text):
    nodes=[n for n in tree.iter('node') if n.get('text')==text]
    assert len(nodes)==1,(text,len(nodes))
    x1,y1,x2,y2=map(int,re.findall(r'\d+',nodes[0].get('bounds')))
    shell(f'input tap {(x1+x2)//2} {(y1+y2)//2}')

original=shell('wm user-rotation').strip()
assert original=='free' or re.fullmatch(r'lock [0-3]',original)
restored=True
try:
    shell('input keyevent KEYCODE_WAKEUP; wm dismiss-keyguard; am start -W -a android.settings.DISPLAY_SETTINGS')
    time.sleep(1)
    tree=dump('display-settings.xml')
    assert any(n.get('text')=='显示与亮度' for n in tree.iter('node')), 'Display settings did not reach the expected foreground page; no swipe performed'
    for _ in range(2):
        if any(n.get('text')=='动画风格' for n in tree.iter('node')):break
        lists=[n for n in tree.iter('node') if n.get('scrollable')=='true']
        assert lists,'No scrollable settings list'
        x1,y1,x2,y2=map(int,re.findall(r'\d+',lists[-1].get('bounds')))
        x=(x1+x2)//2
        shell(f'input touchscreen swipe {x} {y2-150} {x} {y1+180} 800');time.sleep(.5)
        tree=dump('display-settings.xml')
    tap(tree,'动画风格');tree=dump('choices.xml')
    tap(tree,'动画质量' if args.mode=='2' else '动画流畅')
    time.sleep(.5)
    assert shell('getprop persist.sys.oplus.anim_level').strip()==args.mode
    (work/'before-reboot.txt').write_text(shell('cat /proc/sys/kernel/random/boot_id; pidof system_server; getprop persist.sys.oplus.anim_level'),encoding='utf-8')
    # Keep orientation unchanged while the native dialog is open. Changing
    # configuration here recreates Settings and dismisses its transient dialog.
    tree=dump('reboot-dialog.xml')
    tap(tree,'立即重启')
    print('NATIVE_SETTINGS_MODE_SAVED_EXPLICIT_REBOOT_BUTTON_PRESSED',args.mode,flush=True)
finally:
    if not restored:
        shell('wm user-rotation '+original)
    (work/'commands.txt').write_text('\n'.join(commands),encoding='utf-8')
