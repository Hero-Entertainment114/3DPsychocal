"""Create a portable source archive, excluding machine state and build output."""
from pathlib import Path
import zipfile,hashlib
ROOT=Path(__file__).resolve().parents[1]

def main():
    output=ROOT/'dist';output.mkdir(exist_ok=True)
    target=output/'3DPsychocal-source.zip'
    excluded={'.git','.venv','__pycache__','.pytest_cache','saves','dist','build','work'}
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(ROOT.rglob('*')):
            relative=f.relative_to(ROOT)
            if f.is_file() and not set(relative.parts)&excluded and f.suffix not in ('.pyc','.log','.spec'):
                z.write(f,Path('3DPsychocal')/relative)
    (output/'SHA256SUMS.txt').write_text(hashlib.sha256(target.read_bytes()).hexdigest()+'  '+target.name+'\n')
    print(target)
if __name__=='__main__':main()
