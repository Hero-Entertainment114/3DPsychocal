import os,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));os.environ.setdefault('EGL_PLATFORM','surfaceless')
from source.main import Game
from source.core import STORY,State
with tempfile.TemporaryDirectory() as tmp:
 g=Game(headless=True,save_dir=tmp);g.new_game();g.close()
 for i in range(3):
  for n in STORY['chapters'][i]['notes']:g.state.collect(n['id'])
  for p in STORY['chapters'][i]['puzzles']:assert g.state.solve(p['id'],p['answer'])
  g.state.advance()
 g.load_world();g.note('draft');assert 'draft' not in g.state.clues;assert g.world.draft_paper.isHidden()
 g.unlock_cabinet();assert not g.world.draft_paper.isHidden()
 for _ in range(45):g.taskMgr.step()
 assert abs(g.world.drawer.getY()-6.45)<.01
 g.note('draft');assert 'draft' in g.state.clues;g.save('2');g.load('2');assert not g.world.draft_paper.isHidden();assert abs(g.world.drawer.getY()-6.45)<.01
 # Validate a relation whose cards are on different journal pages.
 g.links_panel(0);g.select_pin('photo');g.state.collect('petition');g.links_panel(1);g.select_pin('petition');assert ['petition','photo'] in g.state.links
 assert g.theme=='chapter3';g.menu();assert g.theme=='menu';g.close();assert g.theme=='chapter3'
 g.destroy()
print('PASS: cabinet denies early evidence, key unlocks, drawer animates, document follows drawer, save restores opening, cross-page evidence link, score routing')
