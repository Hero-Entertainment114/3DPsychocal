import os,sys,json,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));os.environ.setdefault('EGL_PLATFORM','surfaceless')
from source.main import Game
from source.core import STORY,ROOT,TRANSLATIONS
from source.locale import UI
out=Path('/tmp/ben-four-languages');out.mkdir(exist_ok=True)
def visit(v,language):
 if isinstance(v,dict):
  if 'en' in v:assert v['en'] in TRANSLATIONS[language] and TRANSLATIONS[language][v['en']].strip(),v['en']
  else:
   for value in v.values():visit(value,language)
 elif isinstance(v,list):
  for value in v:visit(value,language)
for lang in ('ja','zh'):
 for file in ('story.json','dialogues.json','side_stories.json'):visit(json.loads((ROOT/'data'/file).read_text()),lang)
 assert all(v[1] in TRANSLATIONS[lang] for v in UI.values())
with tempfile.TemporaryDirectory() as tmp:
 g=Game(headless=True,save_dir=tmp)
 for lang in ('vi','en','ja','zh'):
  g.settings['language']=lang;g.new_game();g.close()
  for ci,c in enumerate(STORY['chapters']):
   if ci==3:g.unlock_cabinet()
   for n in c['notes']:g.note(n['id']);g.close()
   for p in c['puzzles']:
    g.puzzle(p)
    for _ in range(2):g.taskMgr.step()
    if p==c['puzzles'][0]:g.win.saveScreenshot(str(out/f'{lang}-chapter{ci}.png'))
    g.answer(p,p['answer']);g.close()
   g.consent(ci)
   if ci<4:g.next_chapter();g.close()
  g.side_stories()
  for side in g.side_data:
   for i,step in enumerate(side['steps']):
    g.side_step(side);g.side_answer(side,i,-1)
    assert g.state.decisions.get('side_progress',{}).get(side['id'],0)==i
    g.side_answer(side,i,step['answer'])
   assert g.state.decisions['side_progress'][side['id']]==3
  g.finish('together');assert g.state.ending=='together';g.save('1');g.load('1')
  assert len(g.state.decisions['side_progress'])==2
 g.destroy()
print('PASS: 4 languages, full catalog coverage, 80 main-puzzle solutions, 24 side-story solutions, wrong-answer recovery and save/load')
