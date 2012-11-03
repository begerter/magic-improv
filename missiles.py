import pygame
from pygame.locals import *
from sys import exit
import os,sys, random,math

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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('smallPlayer.png',-1)
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
                print event.key
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

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,index,indrange):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('tinymullet2.png',-1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = x,y
        self.moveRate = 3
        self.ind = index
        self.range = indrange
    def update(self):
        movex = math.cos(2*math.pi*self.ind/self.range)
        movey = math.sin(2*math.pi*self.ind/self.range)
        self.rect.move_ip(movex*self.moveRate, movey*self.moveRate)

class Missile(pygame.sprite.Sprite):
    def __init__(self,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('tinymullet.png',-1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = screen.get_width(), random.randint(0,screen.get_height() - self.rect.height)
        self.moveRate = speed
        self.v = 0.0
        self.counter = 0
        self.indrange = 8
        self.bullets = []
    def update(self):
        self.counter += 1
        self.v += random.random()-0.5
        self.rect.move_ip(-1 * self.moveRate, self.v*self.moveRate)
        if self.counter == random.randint(80,170):
            for i in xrange(self.indrange):
                self.bullets.append(Bullet(self.rect.left,self.rect.top,i,self.indrange))
        if len(self.bullets) > 0:
            for bullet in self.bullets:
                bullet.update()
class Missiles(object):
    def __init__(self, screen, clock, **kwargs):
        self.player = Player()
        self.screen = screen
        self.clock = clock
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        self.screen.blit(self.background, (0,0))
        self.back, self.backRect = load_image('bullethellbg.png',-1)
        self.counter = 0
        pygame.display.flip()
        self.timer = 0
        self.spawnrate = 1
        self.missiles = []
        self.playersprite = pygame.sprite.RenderPlain(self.player)
    def reset(self):
        self.timer = 0
        self.counter = 0
        self.player.up = False
        self.player.down = False
        self.player.left = False
        self.player.right = False
        for missile in self.missiles:
            for bullet in missile.bullets:
                missile.bullets.remove(bullet)
            missile.bullets = []
            self.missiles.remove(missile)
        self.missiles = []
    def update(self, **kwargs):
        self.counter += 1
        if self.counter > 1200:
            self.reset()
            return True
        self.player.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            #if event.type == MOUSEBUTTONDOWN:
                #for missile in self.missiles:
                    #if missile.rect.collidepoint(pygame.mouse.get_pos()):
        for missile in self.missiles:
            for bullet in missile.bullets:
                if bullet.rect.colliderect(self.player.rect):
                    self.reset()
                    return False
            if missile.rect.colliderect(self.player.rect):
                self.reset()
                return False
        self.timer += 1
        self.missiles.append(Missile(random.randint(1,3) + 0.002*random.randint(1,self.timer)))
        for missile in self.missiles:
            missile.update()
            if missile.rect.right < 0:
                self.missiles.remove(missile)
          

    def draw(self, **kwargs):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.back, self.backRect)
        allsprites = pygame.sprite.RenderPlain(self.missiles)
        for missile in self.missiles:
            sprites = pygame.sprite.RenderPlain(missile.bullets)
            sprites.draw(self.screen)
        self.playersprite.draw(self.screen)
        allsprites.draw(self.screen)
        pygame.display.flip()
        
    
 
