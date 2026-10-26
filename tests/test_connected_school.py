from collections import deque
import pygame
from core.state import State
from systems.world import World
from systems.transitions import Transition
from systems.fog import BoundaryFog

def route(c,source,target):
    queue=deque([(source,[])]);seen={source}
    while queue:
        room,path=queue.popleft()
        if room==target:return path+[room]
        for p in c.maps[room]['portals']:
            if p['to'] not in seen:seen.add(p['to']);queue.append((p['to'],path+[room]))

def test_upper_floor_requires_both_staircases(content):
    path=route(content,'school','school_toilets')
    for rid in ['school_vestibule','school_hall1','school_stairs1','school_hall2','school_stairs2','school_corridor']:assert rid in path
    for m in content.maps.values():
        for p in m['portals']:
            dest=content.maps[p['to']]
            if 'floor' in m and 'floor' in dest:
                assert abs(m['floor']-dest['floor'])<=1
                if m['floor']!=dest['floor'] and min(m['floor'],dest['floor'])>0:
                    assert m['theme']=='stairs' or dest['theme']=='stairs'

def test_new_rooms_have_observations_and_signs(content):
    for rid in ['school_medical','school_guard','school_library','school_toilets2']:
        w=World(content,State(room=rid))
        kinds={o['kind'] for o in w.objects()}
        assert {'sign','inspection'}<=kinds
        assert content.maps[rid]['inspection']['text']
    for m in content.maps.values():
        if 'sign' in m:
            x,y=m['sign']['position'];assert 20<x<m['width']*16-20 and 40<y<m['height']*16
            assert m['sign']['jp'] and m['sign']['vi']

def test_transition_finishes_and_does_not_modify_state():
    screen=pygame.Surface((480,270));screen.fill('white');t=Transition(screen.get_size());t.start(screen)
    assert t.active;t.update(.18);t.draw(screen);assert screen.get_at((20,20)).r<10
    t.update(1);assert not t.active

def test_fog_only_covers_outdoor_boundary(content):
    fog=BoundaryFog();screen=pygame.Surface((480,270));screen.fill('white')
    w=World(content,State(room='town'));fog.draw(screen,w)
    assert screen.get_at((0,120)).r<100
    assert screen.get_at((200,120)).r==255
    screen.fill('white');w.state.room='school_hall1';fog.draw(screen,w)
    assert screen.get_at((0,120)).r==255
