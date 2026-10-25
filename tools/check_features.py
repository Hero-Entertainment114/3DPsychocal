import os,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('EGL_PLATFORM','surfaceless')
from source.main import Game
from source.core import STORY
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/ben-features');out.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
 g=Game(headless=True,save_dir=tmp);g.new_game();g.close()
 def capture(name):
  for _ in range(4):g.taskMgr.step()
  assert g.win.saveScreenshot(str(out/(name+'.png')))
 for lang in ['vi','en']:
  g.settings['language']=lang;g.load_world()
  for n in STORY['chapters'][0]['notes']:g.state.collect(n['id'])
  g.links_panel();g.select_pin('calendar');g.select_pin('photo');assert ['calendar','photo'] in g.state.links;capture(lang+'-links')
  g.begin_drag('calendar');g.end_drag()
  g.inspect_item('photo');before=g.inspect_model.getH();g.rotate_item(25);assert g.inspect_model.getH()!=before;capture(lang+'-inspect')
  g.sound_settings();g.setting('music_volume',.15);g.setting('ambience_volume',.8);g.setting('sfx_volume',.4);capture(lang+'-audio')
  g.change_binding('forward');g.apply_binding('forward','q');assert g.settings['bindings']['forward']=='q'
  g.change_binding('forward');g.apply_binding('forward','j');assert g.settings['bindings']['forward']=='q'
  g.bindings_panel();capture(lang+'-bindings');g.settings_done()
  # Real event routing, rather than only a direct key handler.
  g.close();g.camera.setPos(0,-10,1.7);before=g.camera.getY();g.messenger.send('q')
  for _ in range(10):g.taskMgr.step()
  g.messenger.send('q-up');assert g.camera.getY()>before
  for p in STORY['chapters'][0]['puzzles']:assert g.state.solve(p['id'],p['answer'])
  g.state.advance();g.load_world();g.save();original=g.saves.file('auto').read_bytes()
  g.start_replay(0);g.close();g.save();assert g.saves.file('auto').read_bytes()==original;capture(lang+'-replay')
  g.end_replay();assert g.state.chapter==1 and 'replay' not in g.state.decisions
  g.new_game();g.close()
 g.menu();before=g.state.play_seconds
 for _ in range(10):g.taskMgr.step()
 assert g.state.play_seconds==before
 g.destroy()
print('PASS: 2 locales, inspection rotation, evidence linking, audio settings, actual rebound input, replay save isolation, pause-clock exclusion')
