import subprocess, time, re, os, sys
ADB=r"C:\android-sdk\platform-tools\adb.exe"
OUT=sys.argv[1]
LABEL=sys.argv[2] if len(sys.argv)>2 else "run"
os.makedirs(OUT, exist_ok=True)
apps=[
 ("wechat","com.tencent.mm","com.tencent.mm/.ui.LauncherUI"),
 ("douyin","com.ss.android.ugc.aweme","com.ss.android.ugc.aweme/.splash.SplashActivity"),
 ("luna","com.luna.music","com.luna.music/com.luna.biz.main.main.MainActivity"),
]
def sh(*args, timeout=60):
  r=subprocess.run([ADB,*args], capture_output=True, text=True, timeout=timeout)
  return r.stdout
def shell(cmd, timeout=60):
  return sh("shell", cmd, timeout=timeout)

# Ensure apps are open (start without force-stop)
for name,pkg,comp in apps:
  shell(f"am start -n {comp} >/dev/null 2>&1")
  time.sleep(2.5)
# Cycle once to warm
for name,pkg,comp in apps:
  shell(f"am start -n {comp} >/dev/null 2>&1")
  time.sleep(1.5)

summary=[]
for name,pkg,comp in apps:
  shell(f"am start -n {comp} >/dev/null 2>&1")
  time.sleep(2.0)
  # settle with app in foreground
  time.sleep(4.0)
  shell(f"dumpsys gfxinfo {pkg} reset >/dev/null 2>&1")
  # 12 swipes (same as prior headroom)
  for i in range(12):
    shell("input swipe 900 1400 900 500 80")
    time.sleep(0.15)
  time.sleep(0.5)
  gfx=shell(f"dumpsys gfxinfo {pkg}")
  open(os.path.join(OUT,f"gfx-{name}.txt"),"w",encoding="utf-8",errors="replace").write(gfx)
  janky=re.search(r"Janky frames:\s*(\d+)\s*\(([\d.]+)%\)", gfx)
  p50=re.search(r"50th percentile:\s*(\d+)ms", gfx)
  p90=re.search(r"90th percentile:\s*(\d+)ms", gfx)
  p95=re.search(r"95th percentile:\s*(\d+)ms", gfx)
  p99=re.search(r"99th percentile:\s*(\d+)ms", gfx)
  missed=re.search(r"Number Missed Vsync:\s*(\d+)", gfx)
  high=re.search(r"Number High input latency:\s*(\d+)", gfx)
  sm=shell("dumpsys oplusscreenmode")
  open(os.path.join(OUT,f"osm-{name}.txt"),"w",encoding="utf-8",errors="replace").write(sm)
  pr=re.search(r"mCurrentPickRate=([\d.]+)", sm)
  line=f"{name} janky={janky.group(1) if janky else '?'} ({janky.group(2)+'%' if janky else '?'}) p50={p50.group(1) if p50 else '?'}ms p90={p90.group(1) if p90 else '?'}ms p95={p95.group(1) if p95 else '?'}ms p99={p99.group(1) if p99 else '?'}ms missed={missed.group(1) if missed else '?'} high={high.group(1) if high else '?'} PickRate={pr.group(1) if pr else '?'}"
  print(line, flush=True)
  summary.append(line)

sf=shell("dumpsys SurfaceFlinger")
open(os.path.join(OUT,"sf.txt"),"w",encoding="utf-8",errors="replace").write(sf)
open(os.path.join(OUT,"summary.txt"),"w",encoding="utf-8").write("\n".join(summary)+"\n")
# preserve checks
open(os.path.join(OUT,"preserves.txt"),"w",encoding="utf-8").write(
  shell("dumpsys SurfaceFlinger 2>/dev/null | grep -E 'mWorkDuration|activeMode' | head -5")+"\n"+
  shell("settings get system oplus_customize_screen_refresh_rate")+"\n"+
  shell("su -c 'grep appSwitchBoost /my_product/etc/refresh_rate_config.xml; md5sum /my_product/etc/refresh_rate_config.xml'")
)
print("DONE", LABEL, flush=True)
