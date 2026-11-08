import subprocess, time, re, os, sys
ADB=r"C:\android-sdk\platform-tools\adb.exe"
OUT=sys.argv[1]
os.makedirs(OUT, exist_ok=True)

def sh(args, timeout=90):
    r=subprocess.run([ADB]+list(args), capture_output=True, timeout=timeout)
    out=r.stdout.decode("utf-8","replace") if r.stdout else ""
    err=r.stderr.decode("utf-8","replace") if r.stderr else ""
    return out

def shell(cmd, timeout=90):
    return sh(["shell", cmd], timeout=timeout)

apps=[
 ("wechat","com.tencent.mm","com.tencent.mm/.ui.LauncherUI"),
 ("douyin","com.ss.android.ugc.aweme","com.ss.android.ugc.aweme/.splash.SplashActivity"),
 ("luna","com.luna.music","com.luna.music/com.luna.biz.main.main.MainActivity"),
]

# Open all apps (no force-stop) and leave them warm
for name,pkg,comp in apps:
    shell(f"am start -n {comp} >/dev/null 2>&1")
    time.sleep(2.5)

# Warm interrupt cycle: switch among already-open apps
for name,pkg,comp in apps:
    shell(f"am start -n {comp} >/dev/null 2>&1")
    time.sleep(1.2)

summary=[]
# Per-app: switch TO it from another, measure gfx during settle+swipes
order=[0,1,2,0,1,2]  # ensure coming from other app
for idx, (name,pkg,comp) in enumerate(apps):
    # come from a different app first
    other=apps[(idx+1)%3]
    shell(f"am start -n {other[2]} >/dev/null 2>&1")
    time.sleep(1.5)
    shell(f"dumpsys gfxinfo {pkg} reset >/dev/null 2>&1")
    # interrupt TO target (warm, already open)
    shell(f"am start -n {comp} >/dev/null 2>&1")
    time.sleep(1.0)
    for i in range(12):
        shell("input swipe 900 1400 900 500 80")
        time.sleep(0.15)
    time.sleep(0.4)
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
    boost=re.search(r"mAppSwitchBoostType=(\d+)", sm)
    line=f"{name} janky={janky.group(1) if janky else '?'} ({(janky.group(2)+'%') if janky else '?'}) p50={p50.group(1) if p50 else '?'}ms p90={p90.group(1) if p90 else '?'}ms p95={p95.group(1) if p95 else '?'}ms p99={p99.group(1) if p99 else '?'}ms missed={missed.group(1) if missed else '?'} high={high.group(1) if high else '?'} PickRate={pr.group(1) if pr else '?'} type={boost.group(1) if boost else '?'}"
    print(line, flush=True)
    summary.append(line)

# SF key
sf=shell("dumpsys SurfaceFlinger")
keys="\n".join([ln for ln in sf.splitlines() if "mWorkDuration" in ln or "activeMode=" in ln][:8])
open(os.path.join(OUT,"sf-key.txt"),"w",encoding="utf-8").write(keys)
open(os.path.join(OUT,"summary.txt"),"w",encoding="utf-8").write("\n".join(summary)+"\n")
# check boost fired in logcat recent
lc=shell("logcat -d -s RefreshRate:D 2>/dev/null | grep -E 'app switch boost|Trigger app switch|type is 0|startAppSwitchBoost' | tail -40")
open(os.path.join(OUT,"boost-log.txt"),"w",encoding="utf-8",errors="replace").write(lc)
print("DONE B1", flush=True)