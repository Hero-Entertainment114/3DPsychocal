import pygame
from core.state import State
from core.game import Game
from systems.world import World
from systems.lighting import Lighting

def test_every_connection_returns_to_corresponding_door(content):
    for room in content.maps.values():
        for i,p in enumerate(room['portals']):
            s=State(room=room['id'],solved=[p['id'] for p in content.playable]);w=World(content,s)
            assert w.travel(i)
            destination=content.maps[s.room]
            j=next(j for j,q in enumerate(destination['portals']) if q['id']==p['entrance'])
            q=destination['portals'][j]
            assert (s.x,s.y)==(q['x'],q['y']-22)
            assert not w.blocked(s.x,s.y)
            assert w.travel(j)
            assert s.room==room['id'] and (s.x,s.y)==(p['x'],p['y']-22)

def test_light_occlusion_and_range():
    room={'width':8,'height':8,'tiles':[[0]*8 for _ in range(8)]}
    assert Lighting.visible(room,(24,24),(88,24))
    room['tiles'][1][3]=1
    assert not Lighting.visible(room,(24,24),(88,24))

def test_torch_pickup_save_and_one_time_dialogue(tmp_path):
    g=Game(True,tmp_path)
    try:
        g.state.room='shop';g.state.solved=['P001','P002','P003'];g.state.x=280;g.state.y=240
        g.interact()
        assert g.state.inventory.count('Đèn pin đã lắp pin')==1
        assert not any(o['kind']=='pickup' for o in g.world.objects())
        assert g.store.load().flags['flashlight_on']
        g.mode='play';g.handle(pygame.event.Event(pygame.KEYDOWN,key=pygame.K_l,unicode='l'))
        assert not g.store.load().flags['flashlight_on']
        g.state.heard=['D_hiroshi'];g.open_dialogue('D_hiroshi')
        assert g.mode!='dialogue'
        g.state.room='school_store';g.state.x=64;g.state.y=272;g.world.direction=2
        screen=pygame.Surface((480,270));screen.fill('white');g.render.lighting.draw(screen,g.world)
        dark=screen.get_at((85,272-100))
        g.state.flags['flashlight_on']=True;g.world.camera.update(0,100)
        screen.fill('white');g.render.lighting.draw(screen,g.world)
        assert screen.get_at((90,172)).r>dark.r
    finally:pygame.quit()
