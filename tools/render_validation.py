"""Real headless render and UI integration walk-through, not a hardware benchmark."""
import os,sys,tempfile,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('EGL_PLATFORM','surfaceless')
from source.main import Game
from source.core import State,STORY
from collections import deque
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/ben-validation');out.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
 game=Game(headless=True,save_dir=tmp)
 def frame(name):
  for _ in range(3):game.taskMgr.step()
  assert game.win.getXSize()==1280 and game.win.getYSize()==720
  assert game.win.saveScreenshot(str(out/f'{name}.png'))
 def reachable():
  # Flood-fill navigation at 0.5 m resolution, including all table/prop obstacles.
  start=(0,-16);q=deque([start]);visited={start}
  while q:
   x,y=q.popleft()
   for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
    p=(x+dx,y+dy)
    if p not in visited and game.world.walkable(p[0]/2,p[1]/2):visited.add(p);q.append(p)
  for target in game.world.targets:
   x,y,_=target['pos'];assert any((a/2-x)**2+(b/2-y)**2<2.4**2 for a,b in visited),target
  assert not game.world.walkable(12,0)
 for lang in ('vi','en'):
  game.settings['language']=lang;game.new_game();frame(f'{lang}-intro');game.close()
  for ci,c in enumerate(STORY['chapters']):
   assert game.state.chapter==ci;reachable();game.close();frame(f'{lang}-chapter-{ci+1}')
   # Exercise live movement, crouch and camera turning through the update task.
   game.camera.setPos(0,-10,1.7);before=game.camera.getY();game.key('w',True)
   for _ in range(8):game.taskMgr.step()
   game.key('w',False);assert game.camera.getY()>before
   game.key('c',True);game.taskMgr.step();assert game.camera.getZ()<1.2;game.key('c',False)
   if ci==3:game.unlock_cabinet()
   for n in c['notes']:game.note(n['id']);frame(f'{lang}-note-{n["id"]}');game.close()
   for p in c['puzzles']:
    game.puzzle(p);game.hint(p);game.hint(p);frame(f'{lang}-puzzle-{p["id"]}')
    game.answer(p,'WRONG');assert p['id'] not in game.state.solved
    game.answer(p,p['answer']);assert p['id'] in game.state.solved;game.close()
   game.dialogue(ci);frame(f'{lang}-dialogue-{ci}');game.consent(ci)
   game.save('1');game.load('1');assert game.state.complete()
   game.journal();game.map_panel();frame(f'{lang}-map-{ci}');game.close()
   if ci<4:game.next_chapter();game.close()
  for ending in ('silence','alone','together'):
   game.state.ending=None;game.final_choice();game.finish(ending);assert game.state.ending==ending;frame(f'{lang}-ending-{ending}')
  game.menu();frame(f'{lang}-menu');game.settings_panel();frame(f'{lang}-settings')
 print(json.dumps({'locales':2,'chapters_per_locale':5,'puzzles_per_locale':sum(len(c['puzzles']) for c in STORY['chapters']),'endings_per_locale':3,'movement':'passed','collision_reachability':'passed','save_load':'passed','render_size':[1280,720],'screenshots':len(list(out.glob('*.png')))}))
 game.destroy()
