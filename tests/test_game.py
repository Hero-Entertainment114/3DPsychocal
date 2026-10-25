import json
from dataclasses import asdict
import pytest
from source.core import State,Saves,STORY,NOTES,PUZZLES
from source.locale import UI

def complete_chapter(s):
 for n in STORY['chapters'][s.chapter]['notes']:s.collect(n['id'])
 for p in STORY['chapters'][s.chapter]['puzzles']:assert s.solve(p['id'],p['answer'])

def complete_game():
 s=State()
 for chapter in range(5):
  assert s.chapter==chapter;complete_chapter(s)
  if chapter<4:assert s.advance()
 return s

def test_bilingual_content_complete():
 def visit(v):
  if isinstance(v,dict):
   if 'vi' in v:assert set(v)=={'vi','en'} and all(isinstance(x,str) and x.strip() for x in v.values())
   else:
    for value in v.values():visit(value)
  elif isinstance(v,list):
   for value in v:visit(value)
 visit(STORY)
 assert len(STORY['chapters'])==5 and len(PUZZLES)==20 and len(NOTES)==15
 assert all(len(value)==2 and all(value) for value in UI.values())

def test_dependency_graph_has_no_softlock():
 s=complete_game();assert s.complete();assert len(s.solved)==20;assert s.validate()

@pytest.mark.parametrize('choice',['silence','alone','together'])
def test_endings(choice):
 s=complete_game()
 if choice=='together':s.consent=[1,4]
 assert s.finish(choice);assert s.ending==choice;assert s.validate()

def test_consent_required_and_can_be_obtained_late():
 s=complete_game();assert not s.finish('together');s.consent=[4];assert not s.finish('together');s.consent.append(1);assert s.finish('together')

def test_no_advancement_without_evidence():
 s=State();assert not s.advance();assert not s.solve('tin','1708');assert not s.finish('alone')

def test_wrong_answers_recoverable():
 s=State();s.collect('calendar');assert not s.solve('tin','9999');assert s.solve('tin','1708');assert s.solve('tin','1708');assert s.solved==['tin']

def test_puzzles_cannot_skip_order():
 s=State()
 for n in STORY['chapters'][0]['notes']:s.collect(n['id'])
 assert not s.solve('route',1);assert s.solve('tin',' 1708 ');assert s.solve('memory',0);assert s.solve('route',1)

@pytest.mark.parametrize('slot',['auto','1','2','3'])
def test_save_roundtrip_all_progress(tmp_path,slot):
 s=complete_game();s.consent=[1,4];s.finish('together');s.position=[2.5,-3,1.7];s.heading=117;s.decisions['1']='approval'
 saves=Saves(tmp_path);saves.save(s,slot);assert asdict(saves.load(slot))==asdict(s)

def test_corrupt_primary_uses_backup(tmp_path):
 saves=Saves(tmp_path);s=State();saves.save(s);s.collect('calendar');saves.save(s)
 saves.file('auto').write_text('{broken');assert saves.load().clues==[]
 # A subsequent save must not replace the healthy backup with corrupt data.
 saves.save(s);assert json.loads(saves.file('auto').with_suffix('.bak').read_text())['state']['clues']==[]

def test_bad_files_are_rejected(tmp_path):
 saves=Saves(tmp_path);saves.file('1').write_text('{"version":1,"state":{"chapter":50}}')
 with pytest.raises(ValueError):saves.load('1')
 assert not saves.exists('1')

@pytest.mark.parametrize('field,value',[('chapter',-1),('position',[float('nan'),0,0]),('clues',['nonexistent']),('solved',['chain']),('ending','together'),('consent',[99])])
def test_invalid_progress_rejected(field,value):
 s=State();setattr(s,field,value)
 with pytest.raises(ValueError):s.validate()

def test_chapter_transition_spawn_and_preservation():
 s=State();complete_chapter(s);s.position=[3,4,1.2];s.heading=95;s.consent=[0];assert s.advance();assert s.position==[0,-8,1.7];assert s.heading==0;assert len(s.clues)==3;assert s.consent==[0]

def test_links_require_owned_evidence_and_supported_relation():
 from source.investigation import connect
 s=State();assert connect(s,'calendar','photo') is None
 s.collect('calendar');s.collect('photo');s.collect('letter')
 assert connect(s,'calendar','photo');assert connect(s,'photo','calendar');assert len(s.links)==1
 assert connect(s,'calendar','letter') is None
 assert connect(s,'photo','photo') is None

def test_replay_does_not_mutate_campaign_or_unlock_chapters():
 from source.investigation import chapter_snapshot
 s=complete_game();before=asdict(s);replay=chapter_snapshot(s,1)
 assert replay.chapter==1 and replay.decisions['replay'];assert len(replay.solved)==4
 replay.collect('radio');replay.decisions['1']='changed';assert asdict(s)==before
 with pytest.raises(ValueError):chapter_snapshot(State(),1)

def test_new_state_fields_roundtrip(tmp_path):
 from source.investigation import connect
 s=State();s.collect('calendar');s.collect('photo');connect(s,'calendar','photo');s.inspected=['calendar'];s.play_seconds=85.5
 saves=Saves(tmp_path);saves.save(s);assert asdict(saves.load())==asdict(s)

def test_legacy_save_migration(tmp_path):
 s=State();complete_chapter(s);s.advance()
 raw=asdict(s);raw['solved'].remove('reconstruct')
 for k in ('links','inspected','play_seconds'):raw.pop(k)
 saves=Saves(tmp_path);saves.file('1').write_text(json.dumps({'version':1,'state':raw}))
 migrated=saves.load('1');assert migrated.chapter==1 and 'reconstruct' in migrated.solved
 assert migrated.decisions['migrated_from']==1

def test_invalid_evidence_link_rejected():
 s=State();s.links=[['calendar','photo']]
 with pytest.raises(ValueError):s.validate()

def test_additional_conversations_are_bilingual_and_unique():
 from source.core import ROOT
 topics=json.loads((ROOT/'data/dialogues.json').read_text())
 assert len(topics)==5 and all(len(t)==3 for t in topics)
 flat=[t for group in topics for t in group]
 assert len({t['id'] for t in flat})==15
 for t in flat:
  for key in ('title','question','answer'):
   assert set(t[key])=={'vi','en'} and all(t[key].values())
