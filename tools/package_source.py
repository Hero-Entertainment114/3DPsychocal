"""Package real project files with independently verifiable per-file hashes."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'dist';out.mkdir(exist_ok=True)
exclude={'.git','.venv','__pycache__','.pytest_cache','dist','build'}
archive=out/'BenKhongTen_Project_Source_v0_4.zip';manifest=[]
with ZipFile(archive,'w',ZIP_DEFLATED) as z:
 for path in sorted(ROOT.rglob('*')):
  relative=path.relative_to(ROOT)
  if path.is_file() and not path.is_symlink() and not any(p in exclude for p in relative.parts) and path.suffix not in ('.blend1','.pyc'):
   data=path.read_bytes();name=str(Path('BenKhongTen')/relative)
   z.writestr(name,data);manifest.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
 z.writestr('MANIFEST.json',json.dumps({'version':'0.4-development','windowsExecutableIncluded':False,'files':manifest},ensure_ascii=False,indent=2))
with ZipFile(archive) as z:
 assert z.testzip() is None
 for record in json.loads(z.read('MANIFEST.json'))['files']:
  assert hashlib.sha256(z.read(record['path'])).hexdigest()==record['sha256'],record['path']
print(f'Created {archive}: {len(manifest)} verified project files, {archive.stat().st_size} bytes')
(out/(archive.name+'.sha256')).write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+'  '+archive.name+'\n')
