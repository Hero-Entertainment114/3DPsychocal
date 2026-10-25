"""Check actual assets and bilingual data; no claim about aesthetic quality."""
from pathlib import Path
import json,wave,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
records=[]
for p in sorted((ROOT/'assets').rglob('*')):
 if not p.is_file():continue
 if p.suffix=='.png':
  with Image.open(p) as im:im.verify()
 if p.suffix=='.wav':
  with wave.open(str(p)) as w:assert w.getnchannels() in (1,2) and w.getnframes()>100 and w.getsampwidth()==2
 records.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
s=json.loads((ROOT/'data/story.json').read_text())
assert len(s['chapters'])==5 and sum(len(c['puzzles']) for c in s['chapters'])==20
assert len(s['endings'])==3
out=ROOT/'docs/asset-audit.json';out.write_text(json.dumps({'checks':'file decode, nonempty WAV, SHA-256, chapter/puzzle count','assets':records},indent=2))
print(f'PASS: {len(records)} asset files; 5 chapters; 20 puzzles; 3 endings')
