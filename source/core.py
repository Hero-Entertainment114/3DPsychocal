from __future__ import annotations
import json, os, sys, tempfile, shutil
from pathlib import Path
from dataclasses import dataclass, field, asdict
ROOT = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[1]))
STORY = json.loads((ROOT/'data/story.json').read_text(encoding='utf8'))
NOTES = {n['id']:n for c in STORY['chapters'] for n in c['notes']}
PUZZLES = {p['id']:p for c in STORY['chapters'] for p in c['puzzles']}
TRANSLATIONS = json.loads((ROOT/'data/translations.json').read_text(encoding='utf8')) if (ROOT/'data/translations.json').exists() else {}
def tr(value, lang):
 if lang in value:return value[lang]
 return TRANSLATIONS.get(lang,{}).get(value['en'],value['en'])
@dataclass
class State:
 chapter:int=0
 clues:list[str]=field(default_factory=list)
 solved:list[str]=field(default_factory=list)
 consent:list[int]=field(default_factory=list)
 decisions:dict=field(default_factory=dict)
 position:list[float]=field(default_factory=lambda:[0,-8,1.7])
 heading:float=0
 ending:str|None=None
 links:list=field(default_factory=list)
 inspected:list=field(default_factory=list)
 play_seconds:float=0.0
 def collect(self, clue):
  if clue not in NOTES: raise ValueError('Unknown clue')
  if clue not in self.clues:self.clues.append(clue)
 def ready(self,pid):
  p=PUZZLES[pid]; ids=[x['id'] for x in STORY['chapters'][self.chapter]['puzzles']]
  return pid in ids and all(x in self.clues for x in p['requires']) and all(x in self.solved for x in ids[:ids.index(pid)])
 def solve(self,pid,answer):
  if not self.ready(pid): return False
  p=PUZZLES[pid]
  correct=str(answer).strip().replace(',','.')==str(p['answer'])
  if correct and pid not in self.solved:self.solved.append(pid)
  return correct
 def complete(self):return all(p['id'] in self.solved for p in STORY['chapters'][self.chapter]['puzzles'])
 def advance(self):
  if not self.complete() or self.chapter==4:return False
  self.chapter+=1;self.position=[0,-8,1.7];self.heading=0;return True
 def finish(self,choice):
  if self.chapter!=4 or not self.complete():return False
  if choice not in ('silence','alone','together'):return False
  if choice=='together' and not {1,4}.issubset(self.consent):return False
  self.ending=choice;self.decisions['publication']=choice;return True
 def validate(self):
  if type(self.chapter)!=int or not 0<=self.chapter<5:raise ValueError('chapter')
  for values,known in [(self.clues,NOTES),(self.solved,PUZZLES)]:
   if not isinstance(values,list) or len(values)!=len(set(values)) or not all(x in known for x in values):raise ValueError('progress')
  if not isinstance(self.consent,list) or any(type(x)!=int or x not in range(5) for x in self.consent):raise ValueError('consent')
  if type(self.play_seconds) not in (int,float) or not 0<=self.play_seconds<1e9:raise ValueError('playtime')
  if not isinstance(self.inspected,list) or any(x not in self.clues for x in self.inspected):raise ValueError('inspected')
  if not isinstance(self.links,list) or any(not isinstance(pair,list) or len(pair)!=2 or len(set(pair))!=2 or any(x not in self.clues for x in pair) for pair in self.links):raise ValueError('links')
  if not isinstance(self.decisions,dict):raise ValueError('decisions')
  if len(self.position)!=3 or any(type(v) not in (int,float) or not -100<float(v)<100 for v in self.position):raise ValueError('position')
  if type(self.heading) not in (int,float) or not -1e9<self.heading<1e9:raise ValueError('heading')
  if self.ending not in (None,'silence','alone','together'):raise ValueError('ending')
  for c in STORY['chapters'][:self.chapter]:
   if any(p['id'] not in self.solved for p in c['puzzles']):raise ValueError('missing previous chapter')
  for cidx,c in enumerate(STORY['chapters']):
   for idx,p in enumerate(c['puzzles']):
    if p['id'] in self.solved and (cidx>self.chapter or not all(n in self.clues for n in p['requires']) or any(prev['id'] not in self.solved for prev in c['puzzles'][:idx])):raise ValueError('invalid puzzle dependency')
  if self.ending and (self.chapter!=4 or not self.complete() or self.ending=='together' and not {1,4}.issubset(self.consent)):raise ValueError('invalid ending')
  return self
class Saves:
 def __init__(self,path=None):
  self.path=Path(path) if path else Path(os.environ.get('LOCALAPPDATA',Path.home()/'.local/share'))/'BenKhongTen'
  self.path.mkdir(parents=True,exist_ok=True)
 def file(self,slot):
  if slot not in ('auto','1','2','3'):raise ValueError('slot')
  return self.path/f'save-{slot}.json'
 def save(self,state,slot='auto'):
  state.validate();target=self.file(slot)
  payload=json.dumps({'version':2,'state':asdict(state)},ensure_ascii=False)
  fd,tmp=tempfile.mkstemp(dir=self.path,suffix='.tmp')
  try:
   with os.fdopen(fd,'w',encoding='utf8') as f:f.write(payload);f.flush();os.fsync(f.fileno())
   if target.exists():
    try:
     self._read(target)
    except (ValueError,TypeError,KeyError,OSError):pass
    else:shutil.copy2(target,target.with_suffix('.bak'))
   os.replace(tmp,target)
  finally:
   if os.path.exists(tmp):os.unlink(tmp)
 def _read(self,path):
  data=json.loads(path.read_text(encoding='utf8'))
  if data['version'] not in (1,2):raise ValueError('save version')
  raw=data['state']
  if data['version']==1:
   # Previously completed chapters remain traversable after content expansion.
   # Only migrated historical checkpoints receive the new ordering deduction.
   for c in STORY['chapters'][:raw['chapter']+(1 if raw.get('ending') else 0)]:
    for p in c['puzzles']:
     if p['kind']=='sequence' and p['id'] not in raw['solved']:raw['solved'].append(p['id'])
   raw.setdefault('decisions',{})['migrated_from']=1
  return State(**raw).validate()
 def load(self,slot='auto'):
  target=self.file(slot)
  for f in (target,target.with_suffix('.bak')):
   try:return self._read(f)
   except (ValueError,TypeError,KeyError,OSError):continue
  raise ValueError('No valid save or backup')
 def exists(self,slot='auto'):
  try:self.load(slot);return True
  except ValueError:return False
