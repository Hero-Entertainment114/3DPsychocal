import os,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));os.environ.setdefault('EGL_PLATFORM','surfaceless')
from source.main import Game
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/ben-dialogues');out.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
 g=Game(headless=True,save_dir=tmp);g.new_game()
 for lang in ('vi','en'):
  g.settings['language']=lang
  for i in range(5):
   g.conversation_topics(i)
   for topic in g.topics[i]:
    g.conversation_answer(i,topic)
    for _ in range(2):g.taskMgr.step()
    assert g.win.saveScreenshot(str(out/f'{lang}-{topic["id"]}.png'))
 assert len(g.state.decisions['topics'])==15
 g.save('1');g.load('1');assert len(g.state.decisions['topics'])==15
 g.destroy()
print('PASS: 30 conversation renders and persisted reading history')
