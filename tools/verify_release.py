import sys,json,wave
from pathlib import Path
root=Path(sys.argv[1]).resolve()
if not (root/'Game.exe').is_file():raise SystemExit('Missing Game.exe')
if (root/'Game.exe').read_bytes()[:2]!=b'MZ':raise SystemExit('Not a PE executable')
assets=root/'_internal/assets';data=root/'_internal/data'
for name in ['DejaVuSans.ttf','LICENSE-DejaVu.txt','NotoSansCJK-Regular.ttc','LICENSE-NotoCJK.txt']:assert (assets/'fonts'/name).is_file(),name
for name in ['plaster','wood','tile','concrete','paper','roof']:assert (assets/f'textures/{name}.png').is_file(),name
for name in ['memory','rain','paper','step','discovery','menu',*[f'chapter{i}' for i in range(5)],'ending_silence','ending_alone','ending_together']:
 with wave.open(str(assets/f'audio/{name}.wav')) as f:assert f.getnframes()>0
story=json.loads((data/'story.json').read_text(encoding='utf8'));assert len(story['chapters'])==5
assert list((root/'_internal').rglob('*.dll')),'Missing DLLs'
print('Release structure verified. This does not prove Windows runtime compatibility.')
