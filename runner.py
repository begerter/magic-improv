import pygame
from pygame.locals import *
from sys import exit
import os,sys

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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('dude.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.moveRate = 4
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        
    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    self.left = False
                if event.key == K_RIGHT:
                    self.right = False
                if event.key == K_UP:
                    self.up = False
                if event.key == K_DOWN:
                    self.down = False
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.left = True
                if event.key == K_RIGHT:
                    self.right = True
                if event.key == K_UP:
                    self.up = True
                if event.key == K_DOWN:
                    self.down = True
        if self.left and self.rect.left > 0:
                self.rect.move_ip(-1 * self.moveRate, 0)
        if self.right and self.rect.right < self.area.right:
                self.rect.move_ip(self.moveRate, 0)
        if self.up and self.rect.top > 0:
                self.rect.move_ip(0, -1 * self.moveRate)
        if self.down and self.rect.bottom < self.area.bottom:
                self.rect.move_ip(0, self.moveRate)          
class Runner(object):
    def __init__(self, screen, clock, **kwargs):
        self.player = Player()
        self.screen = screen
        self.clock = clock
        self.allsprites = pygame.sprite.RenderPlain(self.player)
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()
    def update(self, **kwargs):
        self.allsprites.update()

    def draw(self, **kwargs):
        self.screen.blit(self.background, (0,0))
        self.allsprites.draw(self.screen)
        pygame.display.flip()
        
    
 
