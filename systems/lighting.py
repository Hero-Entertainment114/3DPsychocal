"""Tile-occluded light field, cached until source, camera or room changes."""
import math
import pygame

class Lighting:
    def __init__(self):
        self.key=None
        self.surface=pygame.Surface((120,68))
        self.output=pygame.Surface((480,270))
    @staticmethod
    def visible(room,source,target):
        dx,dy=target[0]-source[0],target[1]-source[1]
        steps=max(1,int(math.hypot(dx,dy)/6))
        for i in range(1,steps):
            x=int((source[0]+dx*i/steps)//16);y=int((source[1]+dy*i/steps)//16)
            if not 0<=x<room['width'] or not 0<=y<room['height']:return False
            if room['tiles'][y][x] in (1,3):return False
        return True
    def draw(self,screen,world):
        s=world.state;room=world.room
        if not room['id'].startswith('school_'):return
        cam=tuple(int(v) for v in world.camera)
        on=s.flags.get('flashlight_on',False) and 'Đèn pin đã lắp pin' in s.inventory
        key=(s.room,int(s.x)//4,int(s.y)//4,world.direction,on,cam,s.phase)
        if key!=self.key:
            self.key=key
            # Exterior daylight is admitted by the entrance; sealed rooms have no ambient daylight.
            ambient=9 if room['theme'] in ('store','toilets','broadcast') else 23
            self.surface.fill((ambient,ambient,ambient+3))
            facing=((0,1),(-1,0),(1,0),(0,-1))[world.direction]
            for py in range(68):
                for px in range(120):
                    target=(px*4+cam[0],py*4+cam[1]);dx=target[0]-s.x;dy=target[1]-s.y
                    dist=math.hypot(dx,dy)
                    if not on or dist>155:continue
                    dot=(dx*facing[0]+dy*facing[1])/max(1,dist)
                    if dist>15 and dot<.82:continue
                    if not self.visible(room,(s.x,s.y),target):continue
                    brightness=int(ambient+(240-ambient)*(1-dist/155)**.65)
                    self.surface.set_at((px,py),(brightness,brightness,max(ambient,brightness-16)))
            pygame.transform.scale(self.surface,(480,270),self.output)
        screen.blit(self.output,(0,0),special_flags=pygame.BLEND_RGB_MULT)
