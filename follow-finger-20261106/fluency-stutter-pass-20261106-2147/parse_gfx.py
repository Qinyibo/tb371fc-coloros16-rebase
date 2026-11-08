from pathlib import Path
import re
out=Path(r"D:\TB371FC-release\clean-rebase-20261104\follow-finger-20261106\fluency-stutter-pass-20261106-2147")
for p in sorted(out.glob("gfx-*.txt")):
    t=p.read_text(encoding="utf-8", errors="replace")
    print("====", p.name)
    for key in ["Janky frames","50th","90th","95th","99th","Number Missed Vsync","Number High input latency","Total frames"]:
        for line in t.splitlines():
            if key in line:
                print(line.strip())
                break
