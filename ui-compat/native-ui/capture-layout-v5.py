from pathlib import Path
import runpy,time
p=runpy.run_path("camera-compat-native/candidate-app-jni/probe-coloros.py")
shell=p["shell"]
out=Path("ui-compat/native-ui/pad-layout-v5")
out.mkdir(exist_ok=True)
(out/"original.txt").write_text(shell("wm density; wm user-rotation; settings get system font_scale"),encoding="utf-8")
shell("input keyevent KEYCODE_WAKEUP; wm dismiss-keyguard; input keyevent KEYCODE_HOME")
try:
 for density in (380,360):
  shell(f"wm density {density}")
  for rotation,label in ((0,"portrait"),(1,"landscape")):
   shell(f"wm user-rotation lock {rotation}; input keyevent KEYCODE_HOME")
   time.sleep(2)
   remote=f"/data/local/tmp/tb371fc-layout-{density}-{label}.xml"
   shell("uiautomator dump "+remote)
   (out/f"{density}-{label}.xml").write_text(shell("cat "+remote),encoding="utf-8")
   (out/f"{density}-{label}-profile.txt").write_text(shell("dumpsys activity top"),encoding="utf-8")
   import subprocess
   image=subprocess.run(p["ADB"]+["exec-out","screencap -p"],capture_output=True,check=True,timeout=12).stdout
   assert image.startswith(b"\x89PNG")
   (out/f"{density}-{label}.png").write_bytes(image)
finally:
 shell("wm density reset; wm user-rotation free; input keyevent KEYCODE_HOME; input keyevent KEYCODE_SLEEP")
print("LAYOUT_COMPARISON_CAPTURED_DENSITY_OVERRIDE_REMOVED")
