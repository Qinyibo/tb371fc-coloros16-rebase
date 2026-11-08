import re
from pathlib import Path
import sys
p=Path(sys.argv[1])
t=p.read_text(encoding="utf-8",errors="replace")
texts=[x for x in re.findall(r'text="([^"]+)"', t) if x.strip()]
print("FILE", p.name)
print("\n".join(texts))
