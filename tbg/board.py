from __future__ import division
import pygame
from pygame.locals import *
from sys import exit
from .io.mouse import Mouse
import os
WIDTH = 0
HEIGHT= 1
START = ((0,0), (1,1), (3,2))

class Board(object):
  def __init__(self, screen, clock, div=(80,60), **kwargs):
    self.screen = screen
    self.clock  = clock
    self.genBackground(div)
    self.mouse  = Mouse()
    self.selected = None
    self.div = div
    self.eles = dict( (loc, Elephant(tuple(a * b for (a,b) in zip(loc,div)))) for loc in START)
    self.sprites = pygame.sprite.RenderPlain(tuple(self.eles.values()))
  def genBackground(self, div):
    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill((0,0,250))
    size = self.background.get_size()
    for i in xrange(0, size[0], div[0]):
      pygame.draw.line(self.background, (0,0,0), (i, 0), (i, size[1]))
    for i in xrange(0, size[1], div[1]):
      pygame.draw.line(self.background, (0,0,0), (0, i), (size[0], i))
  def update(self, **kwargs):
    self.mouse.tick()
    pos = self.snap(self.mouse.pos)
    loc = self.loc(pos)
    for i in range(0, 2):
      if self.mouse.clicked(i):
        if self.selected == pos:
          self.selected = None
        elif self.selected is None and loc in self.eles:
          self.selected = pos
        elif loc in self.eles:
          return True
        elif self.selected:
          self.eles[self.loc(self.selected)].move(pos)
          self.eles[loc] = self.eles[self.loc(self.selected)]
          del self.eles[self.loc(self.selected)]
          self.selected = None
        else:
          print("No elephant")
          
    self.sprites.update()
  def snap(self, pos):
    return tuple(i - (i % j) for (i, j) in zip(pos, self.div))
  def loc(self, pos):
    return tuple(i // j for (i, j) in zip(pos, self.div))
  def draw(self, **kwargs):
    self.screen.blit(self.background, (0,0))
    if self.selected:
      select = pygame.Surface(self.div)
      select = select.convert()
      select.fill((250,0,0))
      self.screen.blit(select, self.snap(self.selected))
    self.sprites.draw(self.screen)

class Elephant(pygame.sprite.Sprite):
  image = pygame.image.load(os.path.join("assets", "andrewdrewanelephant.png"))
  def __init__(self, loc):
    super(Elephant,self).__init__()
    self.rect = pygame.rect.Rect(loc, self.image.get_size())
  def update(self):
    super(Elephant,self).update()
  def move(self, loc):
    self.rect.topleft = loc
