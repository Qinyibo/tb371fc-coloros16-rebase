"""Capture the fresh-boot desktop at its native display density."""
from pathlib import Path
import json
import re
import subprocess
import time
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"ui-compat/native-ui/pad-layout-v5/runtime-standard-font"
ADB=["D:/TB371FC-release/R94T-v27-r106-20261103-CANDIDATE/tools/adb.exe","-P","5037","-s","REPLACE_WITH_DEVICE_SERIAL"]
def shell(command):
 p=subprocess.run(ADB+["shell",command],check=True,capture_output=True,timeout=20)
 return p.stdout.decode("utf-8","replace").replace("\r","")
OUT.mkdir(exist_ok=False)
boot=shell("cat /proc/sys/kernel/random/boot_id; getprop sys.boot_completed; pidof system_server; pidof com.android.launcher; getenforce; wm size; wm density; settings get system font_scale; wm user-rotation")
(OUT/"boot.txt").write_text(boot,encoding="utf-8")
assert boot.splitlines()[1]=="1" and boot.splitlines()[4]=="Enforcing",boot
assert "Physical density: 360" in boot and "Override density" not in boot
assert boot.splitlines()[-1]=="free"
assert "secure=false" in shell("dumpsys window policy | grep -m1 secure=")
records={}
shell("input keyevent KEYCODE_WAKEUP; wm dismiss-keyguard; input keyevent KEYCODE_HOME")
try:
 for rotation,label in ((0,"portrait"),(1,"landscape")):
  shell(f"wm user-rotation lock {rotation}; input keyevent KEYCODE_HOME")
  time.sleep(2)
  remote="/data/local/tmp/tb371fc-layout-v5.xml"
  shell("uiautomator dump "+remote)
  xml=shell("cat "+remote)
  if 'text="USB 用于"' in xml:
   shell("input keyevent KEYCODE_BACK; input keyevent KEYCODE_HOME")
   shell("uiautomator dump "+remote)
   xml=shell("cat "+remote)
  (OUT/f"{label}.xml").write_text(xml,encoding="utf-8")
  profile=shell("dumpsys activity top")
  (OUT/f"{label}-profile.txt").write_text(profile,encoding="utf-8")
  metrics=[line.strip() for line in profile.splitlines() if re.search(r'ConfigParam.num|availableHeightPx:|cellWidthPx:|cellHeightPx:|icon\(\).getIconSizePx|icon\(\).getIconTextSizePx|workspacePadding\.|hotseatBarSizePx:|workspacePageIndicatorHeight',line)]
  assert any("density=2.25" in line for line in profile.splitlines()),"Launcher retained the old density"
  image=subprocess.run(ADB+["exec-out","screencap -p"],check=True,capture_output=True,timeout=12).stdout
  assert image.startswith(b"\x89PNG")
  (OUT/f"{label}.png").write_bytes(image)
  nodes=ET.fromstring(xml).iter("node")
  capsule=[n.attrib for n in nodes if n.get("resource-id")=="com.android.launcher:id/page_indicator"]
  records[label]={"native_profile":metrics,"capsule":capsule}
finally:
 shell("wm user-rotation free; input keyevent KEYCODE_HOME; input keyevent KEYCODE_SLEEP")
(OUT/"layout.json").write_text(json.dumps(records,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(records,ensure_ascii=False,indent=2))
