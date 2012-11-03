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

def load_sliced_sprites(self, w, h, filename):
    images = []
    master_image = pygame.image.load(os.path.join('assets', filename)).convert_alpha()

    master_width, master_height = master_image.get_size()
    for i in xrange(int(master_width/w)):
    	images.append(master_image.subsurface((i*w,0,w,h)))
    return images,images[0].get_rect()

class Mullet(pygame.sprite.Sprite):
    def __init__(self,x,y,i):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('whackamullet.png',-1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 300 + x*(self.image.get_width() + 50),225 + y*(50 + self.image.get_height())
        self.timer = 0
        self.done = False
        self.index = i
    def update(self):
        self.timer += 1
        if self.timer > random.randint(80,150):
            self.done = True
class WhackAMullet(object):
    def __init__(self, screen, clock, **kwargs):
        self.screen = screen
        self.clock = clock
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        self.screen.blit(self.background, (0,0))
        self.score = 0
        pygame.display.flip()
        self.mullets = [0,0,0,0,0,0,0,0,0]
        self.mulletlist = []
        self.counter = 0
    def reset(self):
        self.counter = 0
        self.mullets = [0,0,0,0,0,0,0,0,0]
        self.score = 0
        self.mulletlist = []
        return True
    def update(self, **kwargs):
        self.counter += 1
        if self.counter > 500:
            if self.score > 1000:
                return True
            return False
        if random.randint(0,100) > 97:
            i = random.randint(0,8)
            if self.mullets[i] == 0:
                row = i % 3
                col = i / 3
                self.mullets[i] = 1
                self.mulletlist.append(Mullet(row,col,i))
        for mullet in self.mulletlist:
            mullet.update()
            if mullet.done:
                self.mulletlist.remove(mullet)
                self.mullets[mullet.index] = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN:
                for mullet in self.mulletlist:
                    if mullet.rect.collidepoint(pygame.mouse.get_pos()):
                        self.score += 100
                        self.mullets[mullet.index] = 0
                        self.mulletlist.remove(mullet)
            for mullet in self.mulletlist:
                mullet.update()          

    def draw(self, **kwargs):
        self.screen.blit(self.background, (0,0))
        allsprites = pygame.sprite.RenderPlain(self.mulletlist)
        allsprites.draw(self.screen)
        pygame.display.flip()
        
    
 
