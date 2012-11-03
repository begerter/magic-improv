import pygame
from pygame.locals import *
from sys import exit
import os,sys, random

def load_image(name, colorkey=None):
    fullname = os.path.join('assets', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Freeze(object):
    def __init__(self, screen, clock, **kwargs):
        self.screen = screen
        self.clock = clock
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()
        self.back, self.backRect = load_image('freeze.png',-1)
        self.counter = 0
    def reset(self):
        self.counter = 0
        return True
    def update(self, **kwargs):
        self.counter += 1
        if self.counter > 500:
            self.reset()
            return True
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP or event.type == KEYDOWN or event.type == KEYUP or event.type == MOUSEMOTION:         
                self.reset()
                return False
    def draw(self, **kwargs):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.back, self.backRect)
        pygame.display.flip()
        
    
 
