#!/bin/bash
set -eu
r=/mnt/d/TB371FC-release/clean-rebase-20261104
python3 - "$r" <<'PY'
from pathlib import Path
import re,json,sys
r=Path(sys.argv[1]);old=Path('/work/tb371fc-wake-20261031/out');new=Path('/work/tb371fc-clean-rebase-r107-erofs-20261104/out')
result=[];count=0
for p in old.rglob('*.o.cmd'):
 q=new/p.relative_to(old)
 if not q.exists():continue
 def macros(p):
  line=p.read_text(errors='replace').splitlines()[0]
  return {x for x in re.findall(r'-D[^ ]+',line) if not x.startswith(('-DBUILD_TAG=', '-DUTS_VERSION=', '-DLINUX_COMPILER='))}
 a,b=macros(p),macros(q);count+=1
 if a!=b:result.append({'object':str(p.relative_to(old)),'only_daily':sorted(a-b),'only_candidate':sorted(b-a)})
out={'scope':'Targeted compiled-object functional -D macro parity; no runtime claim','compared_objects':count,'differences':result}
(r/'wifi-compat/compiled-macro-parity.json').write_text(json.dumps(out,indent=2)+'\n')
print('COMPILED_OBJECTS',count,'FUNCTIONAL_MACRO_DIFFERENCES',len(result))
for row in result[:12]:print(row)
PY
