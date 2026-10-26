"""Outdoor boundary haze follows world edges, never obscures valid doorways."""
import pygame
class BoundaryFog:
    def __init__(self):self.key=None;self.mask=pygame.Surface((480,270),pygame.SRCALPHA)
    def draw(self,screen,world):
        if world.room['theme'] not in ('street','platform','yard'):return
        cx,cy=map(int,world.camera);key=(world.state.room,cx,cy)
        if key!=self.key:
            self.key=key;self.mask.fill((0,0,0,0));width=world.room['width']*16
            for x in range(480):
                distance=min(x+cx,width-1-x-cx)
                if distance<32:
                    alpha=max(0,min(230,int(230*(1-distance/32)**2)))
                    pygame.draw.line(self.mask,(5,10,14,alpha),(x,0),(x,269))
            # Portal approach footprints remain readable even at the perimeter.
            for p in world.room['portals']:
                pygame.draw.rect(self.mask,(0,0,0,0),(p['x']-cx-24,p['y']-cy-32,48,64))
        screen.blit(self.mask,(0,0))
