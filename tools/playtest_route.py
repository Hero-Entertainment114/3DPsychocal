import os,sys,json,time
from pathlib import Path
os.environ['SDL_VIDEODRIVER']='dummy';os.environ['SDL_AUDIODRIVER']='dummy'
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import pygame
from core.game import Game
from collections import deque
import tempfile
qa_temp = tempfile.TemporaryDirectory(prefix='forgotten-voices-qa-')
G=Game(True,Path(qa_temp.name))
G.start();G.mode='play'
report=[];start=time.perf_counter()
def press(k,text=''):G.handle(pygame.event.Event(pygame.KEYDOWN,key=k,unicode=text))
def goal_path(obj):
    w=G.world;s=G.state;start=(round(s.x/4)*4,round(s.y/4)*4);q=deque([start]);parents={start:None};target=None
    while q:
        x,y=q.popleft()
        old=s.x,s.y;s.x,s.y=x,y;nearest=w.nearest();s.x,s.y=old
        if nearest and nearest['kind']==obj['kind'] and nearest['id']==obj['id']:
            target=(x,y);break
        for dx,dy in ((4,0),(-4,0),(0,4),(0,-4)):
            nxt=x+dx,y+dy
            if nxt not in parents and not w.blocked(*nxt):parents[nxt]=(x,y);q.append(nxt)
    assert target,('unreachable',s.room,obj)
    path=[]
    while parents[target] is not None:path.append(target);target=parents[target]
    path.reverse();s.x,s.y=start
    class Keys:
        active=None
        def __getitem__(self,key):return key==self.active
    keys=Keys()
    for x,y in path:
        dx,dy=x-s.x,y-s.y
        keys.active=pygame.K_d if dx>0 else pygame.K_a if dx<0 else pygame.K_s if dy>0 else pygame.K_w
        w.update(4/72,keys)
        assert abs(s.x-x)<.01 and abs(s.y-y)<.01
    return len(path)
def travel(room):
    # Small room graph, enter every transition through its physical portal.
    if G.state.room==room:return
    nextroom=room if G.state.room=='town' else 'town'
    portal=next(o for o in G.world.objects() if o['kind']=='portal' and G.world.room['portals'][int(o['id'])]['to']==nextroom)
    goal_path(portal);press(pygame.K_e);assert G.state.room==nextroom
    if nextroom!=room:travel(room)
for p in G.content.playable:
    travel(p['room'])
    if p['id']=='P014':press(pygame.K_m)
    obj=next(o for o in G.world.objects() if o['kind']=='puzzle' and o['id']==p['id']);steps=goal_path(obj)
    press(pygame.K_e);assert G.mode=='puzzle',(p['id'],G.mode)
    for char in p['answers'][-1]:press(pygame.key.key_code(char),char)
    G.draw()
    if p['id'] in ('P001','P009','P014','P019'):pygame.image.save(G.surface,str(ROOT/'reports'/f'{p["id"]}.png'))
    press(pygame.K_RETURN);assert p['id'] in G.state.solved,p['id']
    if G.mode=='dialogue':
        while not G.choice:press(pygame.K_RETURN)
        press(pygame.K_1)
    if G.mode=='message':press(pygame.K_ESCAPE)
    G.draw();report.append({'puzzle':p['id'],'walk_steps':steps,'mode':G.mode,'room':G.state.room})
assert G.state.flags['slice_complete']
G.toast_time=0;G.draw();pygame.image.save(G.surface,str(ROOT/'reports/school.png'))
G.state.room='town';G.state.x=300;G.state.y=210;G.world.follow(1);G.draw();pygame.image.save(G.surface,str(ROOT/'reports/town.png'))
G.state.room='hospital';G.state.x=220;G.state.y=220;G.world.follow(1);G.open_dialogue('sachiko');G.draw();pygame.image.save(G.surface,str(ROOT/'reports/dialogue.png'))
G.mode='menu';G.selection=0;G.draw();pygame.image.save(G.surface,str(ROOT/'reports/menu.png'))
G.mode='ending';G.ending_id='C';G.ending_page=0;G.draw();pygame.image.save(G.surface,str(ROOT/'reports/ending_preview.png'))
result={'result':'pass','kind':'scripted UI route, not human playtest','duration_seconds':round(time.perf_counter()-start,3),'completed':len(report),'route':report}
(ROOT/'reports/ui_route.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({k:v for k,v in result.items() if k!='route'}))
pygame.quit();qa_temp.cleanup()
