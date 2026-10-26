import math
import pygame

from systems.dialogue import available, choose

class World:
    def __init__(self, content, state):
        self.content, self.state = content, state
        self.camera = pygame.Vector2(0, 0)
        self.direction = 0
        self.walk_time = 0.0
        self.moving = False
    @property
    def room(self): return self.content.maps[self.state.room]
    def actors(self):
        groups={}
        for d in available(self.content,self.state,self.state.room):
            if d['character']!='ren':groups[d['character']]=choose(self.content,self.state,self.state.room,d['character'])
        # An actor with an unheard scene has priority; never pack a room with a cast list.
        rows=sorted(groups.values(),key=lambda d:(d['id'] in self.state.heard,d.get('order',0)))[:2]
        return [dict(kind='npc',id=d['character'],dialogue=d['id'],x=d['position'][0],y=d['position'][1],label=self.content.characters[d['character']]['name']) for d in rows]
    def objects(self):
        s=self.state
        rows=[]
        for p in self.content.playable:
            if p['room'] == s.room and all(d in s.solved for d in p.get('visible_requires',[])):
                x,y=p['position'];rows.append(dict(kind='puzzle',id=p['id'],x=x,y=y,label=p['title']))
        for o in self.content.observations.values():
            if o['room']==s.room and all(d in s.solved for d in o['requires']):
                x,y=o['position'];rows.append(dict(kind='observation',id=o['id'],x=x,y=y,label=o['title']))
        d=choose(self.content,s,s.room,'ren')
        if d:
            x,y=d['position'];rows.append(dict(kind='reflection',id=d['id'],x=x,y=y,label='Dừng lại một chút'))
        for i,p in enumerate(self.room['portals']):
            rows.append(dict(kind='portal',id=str(i),x=p['x'],y=p['y'],label=p['label']))
        return rows+self.actors()
    def nearest(self):
        rows=self.objects()
        if not rows:return None
        row=min(rows,key=lambda o:math.hypot(o['x']-self.state.x,o['y']-self.state.y))
        return row if math.hypot(row['x']-self.state.x,row['y']-self.state.y) <= 39 else None
    def blocked(self,x,y):
        r=pygame.Rect(round(x)-5,round(y)-5,10,7)
        m=self.room
        for ty in range(r.top//16,r.bottom//16+1):
            for tx in range(r.left//16,r.right//16+1):
                if not 0<=tx<m['width'] or not 0<=ty<m['height'] or m['tiles'][ty][tx] in (1,3):return True
        for p in self.content.playable:
            if p['room']==self.state.room and all(d in self.state.solved for d in p.get('visible_requires',[])):
                px,py=p['position']
                if r.colliderect(pygame.Rect(px-12,py-12,24,12)):return True
        return False
    def update(self,dt,keys):
        dx=int(keys[pygame.K_d] or keys[pygame.K_RIGHT])-int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy=int(keys[pygame.K_s] or keys[pygame.K_DOWN])-int(keys[pygame.K_w] or keys[pygame.K_UP])
        self.moving=bool(dx or dy)
        if self.moving:
            self.direction=(2 if dx>0 else 1) if dx else (0 if dy>0 else 3)
            v=pygame.Vector2(dx,dy).normalize()*(108 if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else 72)*dt
            # Substeps protect collision under slow frames and sprinting.
            steps=max(1,math.ceil(v.length()/3))
            for _ in range(steps):
                if not self.blocked(self.state.x+v.x/steps,self.state.y):self.state.x+=v.x/steps
                if not self.blocked(self.state.x,self.state.y+v.y/steps):self.state.y+=v.y/steps
            self.walk_time+=dt
        self.follow(dt)
    def follow(self,dt):
        target=pygame.Vector2(max(0,min(self.room['width']*16-480,self.state.x-240)),max(0,min(self.room['height']*16-270,self.state.y-145)))
        self.camera += (target-self.camera)*min(1,dt*8)
    def travel(self,index):
        p=self.room['portals'][index]
        if p.get('requires') and p['requires'] not in self.state.solved:return False
        self.state.room=p['to'];self.state.x,self.state.y=p['spawn'];self.camera.update(0,0);self.follow(1)
        return True
