from pathlib import Path
import subprocess,time
r=Path.cwd();w=r/'wifi-compat/runtime-channel-fix';w.mkdir(exist_ok=True);a=str(r.parent/'R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe');base=[a,'-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL']
p=subprocess.run(base+['wait-for-device'],capture_output=True,timeout=60);assert p.returncode==0
for n,c in [('early-kernel.txt','dmesg'),('early-status.txt','cat /proc/sys/kernel/random/boot_id; cat /proc/uptime; getprop sys.boot_completed; getprop vendor.wlan.driver.status')]:
 p=subprocess.run(base+['shell',c],capture_output=True,timeout=20);(w/n).write_bytes(p.stdout+p.stderr)
time.sleep(25)
for n,c in [('after-init-kernel.txt','dmesg'),('after-init-status.txt','cat /proc/sys/kernel/random/boot_id; cat /proc/uptime; getprop sys.boot_completed; getprop vendor.wlan.driver.status; ls /sys/class/net; cmd wifi status; settings get global wifi_on'),('after-init-wifi-logcat.txt','logcat -b all -d -v monotonic')]:
 p=subprocess.run(base+['shell',c],capture_output=True,timeout=20);(w/n).write_bytes(p.stdout+p.stderr);print(n,p.returncode,len(p.stdout),flush=True)
