"""Walk all 16 maps, inspect 44 clues, operate 22 puzzles and hear every live scene.
A scripted integration run, not a human duration or editorial playtest.
"""
import os,sys,json,time,math,heapq,tempfile
from pathlib import Path
os.environ['SDL_VIDEODRIVER']='dummy';os.environ['SDL_AUDIODRIVER']='dummy'
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import pygame
from core.game import Game
from systems.dialogue import available
from collections import deque

def run():
    with tempfile.TemporaryDirectory(prefix='forgotten-voices-qa-') as tmp:
        g=Game(True,Path(tmp));g.start();g.mode='play';start=time.perf_counter();visited={g.state.room};route=[]
        def key(name,text=''):
            g.handle(pygame.event.Event(pygame.KEYDOWN,key=pygame.key.key_code(name),unicode=text))
        def walk(obj):
            w=g.world;s=g.state;origin=(round(s.x/4)*4,round(s.y/4)*4);front=[(0,0,origin)];parent={origin:None};cost={origin:0};target=None;objects=w.objects()
            while front:
                _,steps,pos=heapq.heappop(front);x,y=pos
                nearest=min(objects,key=lambda o:(o['x']-x)**2+(o['y']-y)**2)
                if nearest['kind']==obj['kind'] and nearest['id']==obj['id'] and math.hypot(obj['x']-x,obj['y']-y)<=38:
                    target=pos;break
                for dx,dy in ((4,0),(-4,0),(0,4),(0,-4)):
                    nxt=x+dx,y+dy;nc=steps+1
                    if nc<cost.get(nxt,float('inf')) and not w.blocked(*nxt):
                        cost[nxt]=nc;parent[nxt]=pos
                        heapq.heappush(front,(nc+max(0,math.hypot(nxt[0]-obj['x'],nxt[1]-obj['y'])-30)/4,nc,nxt))
            assert target,('unreachable',s.room,obj)
            path=[]
            while parent[target] is not None:path.append(target);target=parent[target]
            path.reverse();s.x,s.y=origin
            class Keys:
                active=None
                def __getitem__(self,k):return k==self.active
            keys=Keys()
            for x,y in path:
                dx,dy=x-s.x,y-s.y;keys.active=pygame.K_d if dx>0 else pygame.K_a if dx<0 else pygame.K_s if dy>0 else pygame.K_w
                w.update(4/72,keys);assert abs(s.x-x)<.01 and abs(s.y-y)<.01
            assert w.nearest()['kind']==obj['kind'] and w.nearest()['id']==obj['id']
            return len(path)
        def map_route(destination):
            q=deque([(g.state.room,[])]);seen={g.state.room}
            while q:
                room,path=q.popleft()
                if room==destination:return path
                for i,p in enumerate(g.content.maps[room]['portals']):
                    if p.get('requires') and p['requires'] not in g.state.solved:continue
                    if p['to'] not in seen:seen.add(p['to']);q.append((p['to'],path+[(room,i,p['to'])]))
            return None
        def travel(destination):
            path=map_route(destination)
            assert path is not None,('locked room',destination,g.state.solved)
            for room,index,dest in path:
                obj=next(o for o in g.world.objects() if o['kind']=='portal' and o['id']==str(index));walk(obj);key('e')
                assert g.state.room==dest and g.mode=='play';visited.add(dest)
        def finish_dialogue():
            did=g.dialogue['id']
            guard=0
            while not g.choice:
                key('return');guard+=1;assert guard<200
            key('1');assert did in g.state.heard
        def drain():
            while True:
                progress=False
                for d in available(g.content,g.state):
                    if d['id'] in g.state.heard or map_route(d['room']) is None:continue
                    travel(d['room'])
                    obj=next((o for o in g.world.objects() if (o['kind']=='npc' and o['dialogue']==d['id']) or (o['kind']=='reflection' and o['id']==d['id'])),None)
                    if not obj:continue
                    walk(obj);key('e');assert g.mode=='dialogue' and g.dialogue['id']==d['id'];finish_dialogue();progress=True
                if not progress:break
        def operate(p):
            actions={'basket':['1','2','3'],'battery':['space'],'sequence':['2','3','4'],'wires':['2','1','3'],'rhythm':['space','space','right','space'],'dials':['up']*4+['right']+['up']*4+['right']+['up']*4,'count':['up'],'doors':['3'],'latch':['left','down']}
            if p['mechanic'] in actions:
                for name in actions[p['mechanic']]:key(name,name if len(name)==1 else '')
            else:
                for char in p['answers'][-1]:key(char,char)
        for p in g.content.playable:
            drain()
            for oid in p['observations']:
                note=g.content.observations[oid];travel(note['room']);obj=next(o for o in g.world.objects() if o['kind']=='observation' and o['id']==oid)
                walk(obj);key('e');assert g.mode=='message';key('escape');assert g.state.flags['observed_'+oid]
            travel(p['room'])
            if p['id']=='P014' and not g.state.memory:key('m')
            obj=next(o for o in g.world.objects() if o['kind']=='puzzle' and o['id']==p['id']);steps=walk(obj);key('e');assert g.mode=='puzzle';operate(p)
            g.toast_time=0;g.draw()
            if p['id'] in ('P003','P009','P012','P013','P016','P021'):pygame.image.save(g.surface,str(ROOT/'reports'/f'{p["id"]}.png'))
            key('return');assert p['id'] in g.state.solved,(p['id'],g.toast)
            if g.mode=='dialogue':finish_dialogue()
            if g.mode=='message':key('escape')
            if p['id']=='P014' and g.state.memory:key('m')
            route.append({'puzzle':p['id'],'room':g.state.room,'approach_steps':steps,'heard_so_far':len(g.state.heard)})
        drain()
        assert len(visited)==16,visited
        assert len(g.state.heard)==sum(d['status']=='playable' for d in g.content.dialogues.values())
        assert g.state.flags['slice_complete']
        g.save();assert g.store.load().snapshot()==g.state.snapshot()
        for room in ('station','shop','hospital','school','school_class','school_toilets'):
            travel(room);g.toast_time=0;g.draw();pygame.image.save(g.surface,str(ROOT/'reports'/f'{room}.png'))
        g.open_dialogue('D_walk_home');g.dialogue_index=0;g.toast_time=0;g.draw();pygame.image.save(g.surface,str(ROOT/'reports/dialogue.png'))
        g.mode='menu';g.selection=0;g.draw();pygame.image.save(g.surface,str(ROOT/'reports/menu.png'))
        report={'result':'pass','kind':'scripted full input route, not human playtest','duration_seconds':round(time.perf_counter()-start,3),'completed_puzzles':len(route),'visited_maps':sorted(visited),'observations':sum(g.state.flags.get('observed_'+o,False) for o in g.content.observations),'conversations_heard':len(g.state.heard),'spoken_units_reachable':sum(len(l['text'].split()) for did in g.state.heard for l in g.content.dialogues[did]['lines']),'route':route}
        (ROOT/'reports/ui_route.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({k:v for k,v in report.items() if k!='route'}));pygame.quit()
if __name__=='__main__':run()
