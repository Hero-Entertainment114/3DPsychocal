import logging
import pygame
from core.paths import ROOT

class Audio:
    def __init__(self, settings):
        self.settings=settings
        self.enabled=False
        self.sounds={}
        self.track=None
        try:
            pygame.mixer.init(frequency=22050,buffer=512)
            for key in ('step','knock','chime','rain','hum'):
                self.sounds[key]=pygame.mixer.Sound(str(ROOT/'assets/audio'/f'{key}.wav'))
            self.enabled=True
        except pygame.error: logging.warning('Audio unavailable; visual sound captions remain enabled.')
    def play(self,name):
        if not self.enabled:return
        self.sounds[name].set_volume(self.settings['master']*self.settings['effects']*.65)
        self.sounds[name].play()
    def music(self,chapter=0):
        if not self.enabled:return
        if chapter!=self.track:
            path=ROOT/'assets/music'/('sixth_name.wav' if chapter==6 else f'chapter_{chapter}.wav')
            pygame.mixer.music.load(str(path));pygame.mixer.music.play(-1);self.track=chapter
        pygame.mixer.music.set_volume(self.settings['master']*self.settings['music'])
    def ambience(self,name):
        if not self.enabled:return
        c=pygame.mixer.Channel(1);c.stop();c.set_volume(self.settings['master']*self.settings['effects']*.45);c.play(self.sounds[name],loops=-1)
    def refresh(self):
        if self.enabled:
            pygame.mixer.music.set_volume(self.settings['master']*self.settings['music'])
            pygame.mixer.Channel(1).set_volume(self.settings['master']*self.settings['effects']*.45)
