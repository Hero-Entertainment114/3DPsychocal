"""Brief doorway fade; input pauses, save positions remain at the arrival door."""
import pygame
class Transition:
    duration=.36
    def __init__(self,size):
        self.remaining=0.;self.previous=pygame.Surface(size);self.shade=pygame.Surface(size)
        self.shade.fill((4,7,10))
    @property
    def active(self):return self.remaining>0
    def start(self,screen):self.previous.blit(screen,(0,0));self.remaining=self.duration
    def update(self,dt):self.remaining=max(0,self.remaining-dt)
    def draw(self,screen):
        if not self.active:return
        fraction=1-self.remaining/self.duration
        if fraction<.5:screen.blit(self.previous,(0,0))
        self.shade.set_alpha(round(255*(1-abs(2*fraction-1))));screen.blit(self.shade,(0,0))
