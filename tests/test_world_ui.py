from collections import deque
import pygame
import pytest
from core.state import State
from systems.world import World
from core.game import Game

def reachable_positions(w,start):
    start=(int(start[0]//4)*4,int(start[1]//4)*4)
    q=deque([start]);seen={start}
    while q:
        x,y=q.popleft()
        for dx,dy in ((4,0),(-4,0),(0,4),(0,-4)):
            p=x+dx,y+dy
            if p not in seen and not w.blocked(*p):seen.add(p);q.append(p)
    return seen

def test_every_hotspot_and_exit_can_be_reached(content):
    for rid,m in content.maps.items():
        s=State(room=rid,x=64,y=280);w=World(content,s)
        start=(96,172) if rid=='station' else (80,240)
        assert not w.blocked(*start),rid
        seen=reachable_positions(w,start)
        for obj in w.objects():
            assert any((x-obj['x'])**2+(y-obj['y'])**2<=38**2 for x,y in seen),(rid,obj)
        for portal in m['portals']:
            dest=World(content,State(room=portal['to']))
            assert not dest.blocked(*portal['spawn']),(rid,portal)

def test_collision_and_diagonal_motion(content):
    w=World(content,State(x=22,y=80));before=w.state.x
    class Keys:
        def __getitem__(self,k):return k==pygame.K_a
    w.update(.5,Keys());assert w.state.x>=21 and w.state.x<=before
    assert w.blocked(-1,100)

@pytest.fixture
def game(tmp_path):
    g=Game(True,tmp_path);yield g;pygame.quit()

def key(g,k,text=''):
    g.handle(pygame.event.Event(pygame.KEYDOWN,key=k,unicode=text))

def test_menu_dialogue_puzzle_and_pause_through_input(game):
    g=game;key(g,pygame.K_RETURN);assert g.mode=='message'
    key(g,pygame.K_ESCAPE);assert g.mode=='play'
    g.state.x=224;g.state.y=140;key(g,pygame.K_e);assert g.mode=='puzzle'
    key(g,pygame.K_2,'2');key(g,pygame.K_RETURN);assert 'P001' in g.state.solved
    g.state.x=140;g.state.y=230;key(g,pygame.K_e);assert g.mode=='dialogue'
    while not g.choice:key(g,pygame.K_RETURN)
    key(g,pygame.K_1);assert g.state.relations['hiroshi']['trust']==2
    key(g,pygame.K_ESCAPE);assert g.mode=='pause';before=(g.state.x,g.state.y,g.state.play_seconds);g.update(1);assert (g.state.x,g.state.y,g.state.play_seconds)==before
    key(g,pygame.K_ESCAPE);assert g.mode=='play'

def test_draw_every_screen_and_all_text_pages(game):
    g=game
    for mode in ('menu','play','pause','settings','save','load','inventory','journal','chapters','extras','new_confirm'):
        g.mode=mode;g.draw()
    for d in g.content.dialogues.values():
        g.open_dialogue(d['character'])
        for i,page in enumerate(g.dialogue_pages):
            assert len(page[1])<=6
            assert all(g.render.fonts[11].size(line)[0]<=305 for line in page[1])
            g.dialogue_index=i;g.draw()
    for p in g.content.playable:
        g.pid=p['id'];g.mode='puzzle';g.draw()
        height=len(g.render.wrap(p['prompt'],414,11))*15+sum(len(g.render.wrap('— '+c,414,10))*14+5 for c in p['clues'])
        assert height<=133,p['id']
    for e in 'ABCDE':
        g.ending_id=e;g.mode='ending'
        for page in range(8):g.ending_page=page;g.draw()

def test_memory_required_for_observation_puzzle(game):
    g=game
    for p in g.content.playable[:13]:g.progress.solve(p['id'],p['answers'][-1])
    g.state.room='school';g.pid='P014';g.input='2';g.answer();assert 'P014' not in g.state.solved
    g.mode='play';key(g,pygame.K_m);assert g.state.flags['school_memory_seen']
    g.answer();assert 'P014' in g.state.solved

def test_settings_keys_and_persistence(game):
    g=game;g.mode='settings';g.selection=10;key(g,pygame.K_RETURN);key(g,pygame.K_q,'q')
    assert g.settings['keys']['interact']=='q'
    assert g.store.settings()['keys']['interact']=='q'
    g.selection=0;key(g,pygame.K_LEFT);assert g.settings['master']==.6
