import json
import pytest
from core.state import State
from systems.progression import Progression,select_ending,ending_fixture
from systems.storage import Storage,SaveError,validate
from tools.validate_content import validate as validate_content

def prepare_observations(state,puzzle):
    for oid in puzzle['observations']:state.flags['observed_'+oid]=True
    if puzzle['id']=='P014':state.flags['school_memory_seen']=True

def test_content_graph_and_references(content):
    assert validate_content(content)['errors']==[]

def test_playable_route_each_checkpoint_reloads(content,tmp_path):
    state=State();store=Storage(tmp_path,content)
    for p in content.playable:
        prog=Progression(content,state)
        assert prog.available(p['id']),p['id']
        prepare_observations(state,p)
        assert prog.solve(p['id'],p['answers'][-1])
        before=state.snapshot();store.save(state);state=store.load();assert state.snapshot()==before
    assert len(state.solved)==22 and state.flags['slice_complete']
    assert state.chapter==1 and state.phase=='dawn'
    assert select_ending(state) is None

def test_wrong_answers_skip_and_idempotence(content):
    s=State();p=Progression(content,s)
    assert not p.solve('P002','2')
    assert not p.solve('P001','wrong',assisted=True)
    for _ in range(3):assert not p.solve('P001','wrong')
    assert p.solve('P001','',assisted=True)
    before=s.snapshot();assert p.solve('P001','wrong');assert s.snapshot()==before
    assert s.choices['P001']=='assisted'

def test_both_moral_answers_progress_without_softlock(content):
    for answer in ('1','2'):
        s=State();p=Progression(content,s)
        for item in content.playable:
            prepare_observations(s,item)
            assert p.solve(item['id'],answer if item['id']=='P018' else item['answers'][-1])
        assert s.flags['heard_child']==(answer=='2')
        assert s.guilt==(1 if answer=='1' else 0)

def test_relation_persists_and_cannot_be_farmed(content):
    s=State();p=Progression(content,s);p.relationship('yui','listen');p.relationship('yui','repeat')
    assert s.relations['yui']['trust']==2
    assert s.guilt==0
    p.relationship('tomoko','repeat');assert s.flags['rumor_spread']

def test_combining_evidence_retry_and_dedup(content):
    s=State(evidence=['E007','E015','E003']);p=Progression(content,s)
    assert not p.combine('E007','E007')
    assert not p.combine('E007','E003')
    assert p.combine('E015','E007');assert s.clarity==2
    assert p.combine('E007','E015');assert s.clarity==2
    assert s.flags['corroborated']

@pytest.mark.parametrize('ending',list('ABCDE'))
def test_ending_rules_are_distinct(content,ending):
    s=ending_fixture(ending,State());assert select_ending(s)==ending
    e=content.endings[ending];assert len(e['scenes'])==3;assert len(e['epilogues'])==10

def test_save_roundtrip_full_state(content,tmp_path):
    s=State();p=Progression(content,s);prepare_observations(s,content.puzzles['P001']);assert p.solve('P001','2');p.relationship('yui','repeat')
    s.memory=True;s.play_seconds=123.4;s.hints['P001']=2
    store=Storage(tmp_path,content)
    for slot in ('auto','1','2','3'):
        store.save(s,slot);assert store.load(slot).snapshot()==s.snapshot()
    assert not list(tmp_path.glob('*.tmp'))

@pytest.mark.parametrize('mutation',[
    lambda d:d.update(schema=999),lambda d:d.update(x=float('nan')),
    lambda d:d.update(room='missing'),lambda d:d.update(solved=['P099']),
    lambda d:d.update(solved=['P022']),lambda d:d.update(fear=-1),
    lambda d:d.update(relations={'yui':{'trust':'high'}}),lambda d:d.update(attempts={'P001':-1}),
    lambda d:d.update(x=True),lambda d:d.update(choices={'x':None}),
    lambda d:d.update(heard=['D_missing']),lambda d:d.update(evidence=['E999']),
    lambda d:d.update(hints={'P001':99}),lambda d:d.update(y=45),
    lambda d:d.update(chapter=0.5),
])
def test_invalid_save_rejected(content,mutation):
    d=State().snapshot();mutation(d)
    with pytest.raises(SaveError):validate(d,content)

def test_corrupt_save_is_not_overwritten(content,tmp_path):
    path=tmp_path/'save_auto.json';path.write_text('{oops',encoding='utf8');store=Storage(tmp_path,content)
    with pytest.raises(SaveError):store.load()
    assert path.read_text()=='{oops'

def test_settings_malformed_types_are_ignored(content,tmp_path):
    (tmp_path/'settings.json').write_text('{"master": "LOUD", "keys": [], "crt": "yes"}')
    s=Storage(tmp_path,content).settings();assert s['master']==.7 and s['crt'] is False
