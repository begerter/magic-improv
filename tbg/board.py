from __future__ import division
import pygame
from pygame.locals import *
from sys import exit
from .io.mouse import Mouse
import os
from .units.dude import Dude
from .units.zombie import Zombie
WIDTH = 0
HEIGHT= 1
UNITS = (((0,0), (1,1), (3,2)), Dude), (((4,4), (5,5), (2,3)), Zombie)

class Board(object):
  def __init__(self, screen, clock, div=(60,60), **kwargs):
    self.screen = screen
    self.clock  = clock
    self.genBackground(div)
    self.mouse  = Mouse()
    self.selected = None
    self.div = div
    self.units = dict( (loc, type(loc=loc,board=self)) for (group, type) in UNITS for loc in group)
    self.sprites = pygame.sprite.RenderPlain(tuple(self.units.values()))
  def genBackground(self, div):
    self.background = pygame.Surface((600,600))
    self.background = self.background.convert()
    self.background.fill((0,0,250))
    size = self.background.get_size()
    for i in xrange(0, size[0], div[0]):
      pygame.draw.line(self.background, (0,0,0), (i, 0), (i, size[1]))
    for i in xrange(0, size[1], div[1]):
      pygame.draw.line(self.background, (0,0,0), (0, i), (size[0], i))
  def update(self, result=None, **kwargs):
    self.mouse.tick()
    loc = self.loc(self.mouse.pos)
    for i in range(0, 2):
      if self.mouse.clicked(i):
        if self.selected == loc:
          self.selected = None
        elif self.selected is None and loc in self.units:
          self.selected = loc
        elif loc in self.units:
          result = (self.units[self.selected], self.units[loc])
          self.selected = None
          return result
        elif self.selected:
          self.units[self.selected].move(loc)
          self.units[loc] = self.units[self.selected]
          del self.units[self.selected]
          self.selected = None
    self.sprites.update()
    # eat queue becuase why not
    for event in pygame.event.get():
      if event.type == QUIT:
        raise Exception("Quitting")
  def snap(self, pos):
    return tuple(i - (i % j) for (i, j) in zip(pos, self.div))
  def loc(self, pos):
    return tuple(i // j for (i, j) in zip(pos, self.div))
  def pos(self, loc):
    return tuple(i * j for (i,j) in zip(loc, self.div))
  def draw(self, **kwargs):
    self.screen.blit(self.background, (0,0))
    if self.selected:
      select = pygame.Surface(self.div)
      select = select.convert()
      select.fill((250,0,0))
      self.screen.blit(select, self.pos(self.selected))
    self.sprites.draw(self.screen)

