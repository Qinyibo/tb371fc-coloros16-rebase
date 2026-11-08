import zipfile
from pathlib import Path
import sys
mod = Path(sys.argv[1])
zip_path = Path(sys.argv[2])
if zip_path.exists():
    zip_path.unlink()
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for p in mod.rglob('*'):
        if p.is_file():
            arc = p.relative_to(mod).as_posix()
            z.write(p, arcname=arc)
print('zip', zip_path, zip_path.stat().st_size)
# list roots
with zipfile.ZipFile(zip_path) as z:
    print('roots', sorted({n.split('/')[0] for n in z.namelist()}))
