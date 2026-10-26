from collections import Counter
import json,hashlib
import pytest
from core.state import State
from systems.progression import Progression
from systems.dialogue import choose,complete,available
from systems.mechanics import Mechanism
from systems.storage import Storage,SaveError
from systems.world import World
from tools.narrative_audit import audit

def test_chapter_structure_and_distinct_eight_maps(content):
    assert len(content.chapters)==8
    counts=Counter(m['chapter'] for m in content.maps.values())
    assert counts[0]==8 and counts[1]==8
    hashes={hashlib.sha256((content.root/'assets/maps'/f'{m["id"]}.png').read_bytes()).hexdigest() for m in content.maps.values()}
    assert len(hashes)==16
    assert all(m['purpose'] and m['portals'] for m in content.maps.values())

def test_dialogue_release_gate_and_anchored_clues(content):
    result=audit(content)
    assert not result['errors']
    assert result['per_chapter_spoken_units'][0]>=6000
    assert result['per_chapter_spoken_units'][1]>=7500
    assert result['duplicate_spoken_units']==0
    assert result['dialogue_budget']==50000
    assert not result['full_release_ready']
    assert not result['release_gates']['45000_playable_nonduplicate_spoken_units']

def test_invalid_clue_quote_is_detected(content):
    content.dialogues['D_arrival']['clue_links'][0]['quote']='This sentence is not spoken.'
    assert any('not anchored' in e for e in audit(content)['errors'])

def test_dialogue_cycle_is_detected(content):
    content.dialogues['D_arrival']['after_dialogues']=['D_arrival']
    assert any('Unreachable' in e for e in audit(content)['errors'])

def test_story_gate_and_conversation_consequence_cannot_be_farmed(content):
    s=State();assert choose(content,s,'station','hiroshi')['id']=='D_hiroshi'
    assert not complete(content,s,'D_route_east','listen')
    assert complete(content,s,'D_hiroshi','listen')
    assert choose(content,s,'station','hiroshi')['id']=='D_arrival'
    before=s.snapshot();assert not complete(content,s,'D_hiroshi','repeat');assert s.snapshot()==before
    assert complete(content,s,'D_arrival','repeat');assert s.flags['rumor_spread']

def test_unseen_clues_cannot_be_bypassed_by_knowing_answer(content):
    s=State();p=Progression(content,s)
    assert not p.solve('P001','2')
    s.flags['observed_P001a']=True
    assert not p.solve('P001','2')
    s.flags['observed_P001b']=True
    assert p.solve('P001','2')

def test_future_clues_and_people_not_dumped_on_arrival(content):
    s=State(room='school_store');w=World(content,s)
    assert not any(o['kind'] in ('puzzle','observation') for o in w.objects())
    s.solved=[p['id'] for p in content.playable]
    assert any(o['kind']=='observation' for o in w.objects())
    for rid in content.maps:
        s.room=rid;assert len(w.actors())<=2

def test_old_save_is_migrated_and_backed_up(content,tmp_path):
    old=State().snapshot();old.update(schema=1,room='school',x=544,y=192,solved=[p['id'] for p in content.playable])
    raw=json.dumps(old,ensure_ascii=False);target=tmp_path/'save_auto.json';target.write_text(raw,encoding='utf8')
    storage=Storage(tmp_path,content);new=storage.load()
    assert new.schema==2 and (new.x,new.y)==tuple(content.maps['school']['entry'])
    assert all(new.flags['observed_'+o] for o in content.observations)
    assert target.read_text(encoding='utf8')==raw
    assert target.with_suffix('.v1.bak').read_text(encoding='utf8')==raw
    storage.save(new);assert storage.load().snapshot()==new.snapshot()

def test_corrupt_legacy_coordinates_not_silently_repaired(content,tmp_path):
    old=State().snapshot();old.update(schema=1,x=float('nan'))
    target=tmp_path/'save_auto.json';target.write_text(json.dumps(old))
    with pytest.raises(SaveError):Storage(tmp_path,content).load()
    assert not target.with_suffix('.v1.bak').exists()

@pytest.mark.parametrize('pid,keys,answer',[
    ('P003',['1','2','3'],'400'),('P006',['space'],'-'),('P009',['2','3','4'],'234'),
    ('P012',['2','1','3'],'213'),('P013',['space','space','right','space'],'21'),
    ('P016',['up']*4+['right']+['up']*4+['right']+['up']*4,'444'),
    ('P017',['up'],'1'),('P020',['3'],'3'),('P021',['left','down'],'2'),
])
def test_mechanisms_are_operable_through_input(content,pid,keys,answer):
    model=Mechanism(content.puzzles[pid])
    for k in keys:model.key(k)
    assert model.answer()==answer

def test_rhythm_requires_pause_and_latch_requires_order(content):
    rhythm=Mechanism(content.puzzles['P013'])
    for k in ['space']*3:rhythm.key(k)
    assert rhythm.answer()!='21'
    latch=Mechanism(content.puzzles['P021']);latch.key('down');assert latch.answer()!='2'
    latch.key('left');assert latch.answer()!='2';latch.key('down');assert latch.answer()=='2'
