from pathlib import Path
import subprocess,time,json
r=Path.cwd();w=r/'wifi-compat';adb=str(r.parent/'R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe');fb=str(r/'flash-network-candidate/tools/fastboot.exe')
p=subprocess.run([adb,'-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL','shell','getprop sys.boot_completed; cat /proc/sys/kernel/random/boot_id'],capture_output=True,timeout=12);print(p.stdout.decode(errors='replace'),flush=True);assert p.returncode==0 and p.stdout.startswith(b'1')
p=subprocess.run([adb,'-P','5037','-s','REPLACE_WITH_DEVICE_SERIAL','reboot','bootloader'],capture_output=True,timeout=12);print('REBOOT_BOOTLOADER',p.returncode,flush=True)
time.sleep(3)
p=subprocess.run([fb,'-s','REPLACE_WITH_DEVICE_SERIAL','getvar','product'],capture_output=True,timeout=12);(w/'fastboot-entry.txt').write_bytes(p.stdout+p.stderr);print((p.stdout+p.stderr).decode(errors='replace'),flush=True);assert p.returncode==0
