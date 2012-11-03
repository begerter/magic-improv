from __future__ import division
import pygame
from pygame.locals import *
from sys import exit
from .io.mouse import Mouse
import os
import itertools
from .terrain.terrain import Terrain
from .terrain.base import Base
from .units.protag import Protag
from .units.archer import Archer
from .units.dude import Dude
from .units.zombie import Zombie
from .units.mullet import Mullet
import random

WIDTH = 0
HEIGHT= 1
UNITS = (((0,0),), Protag), (((0,1),), Archer), (((1,1), (3,2)), Dude), (((4,4), (5,5), (2,3)), Zombie), (((6,6),), Mullet)

END_TURN = pygame.image.load(os.path.join("assets", "end.png"))
class endButton(pygame.sprite.Sprite):
  def __init__(self):
    super(endButton, self).__init__()
    self.image = END_TURN
    self.rect = pygame.rect.Rect((600,500), self.image.get_size())
    

class Board(object):
  def __init__(self, screen, clock, div=(60,60), **kwargs):
    super(Board, self).__init__(**kwargs)
    self.screen = screen
    self.clock  = clock
    self.genBackground(div)
    self.mouse  = Mouse()
    self.selected = None
    self.div = div
    self.terrain = Terrain(self)
    self.units = dict( (loc, type(loc=loc,board=self)) for (group, type) in UNITS for loc in group)
    self.unitsr   = pygame.sprite.RenderPlain(tuple(self.units.values()))
    self.endr = pygame.sprite.RenderPlain((endButton(),))
    self.ai = -1
  def genBackground(self, div):
    self.background = pygame.Surface((800,600))
    self.background = self.background.convert()
    self.background.fill((0,0,0))
    size = self.background.get_size()
    for i in xrange(0, size[0], div[0]):
      pygame.draw.line(self.background, (0,0,0), (i, 0), (i, size[1]))
    for i in xrange(0, size[1], div[1]):
      pygame.draw.line(self.background, (0,0,0), (0, i), (size[0], i))
  def clearSelection(self):
    self.selected = None
    self.terrain.clear()
  def update(self, result=None, **kwargs):
    if result is None:
      try:
        self.mouse.tick()
        loc = self.loc(self.mouse.pos)
        while self.ai >= 0:
          self.ai += 1
          if self.ai == 600000:
            self.ai = 0
            for enemy in self.units.values():
              if enemy.side == 1:
                for yours in self.units.values():
                  if yours.side == 0 and sum(abs(i-j) for (i,j) in zip(enemy.loc, yours.loc)) == enemy.range and not enemy.attacked:
                    enemy.attacked = True
                    enemy.movement = 0
                    self.result = (yours, enemy)
                    return self.result
            changed = False
            for enemy in self.units.values():
              if enemy.side == 1 and enemy.movement > 0:
                possibilities = []
                for (i,j) in ((1,0),(0,1),(-1,0),(0,-1)):
                  nloc = enemy.loc[0] + i, enemy.loc[1] + j
                  if nloc in self.terrain.table and nloc not in self.units and self.terrain.table[nloc].cost != -1:
                    possibilities.append(nloc)
                    self.terrain.table[nloc].left = self.terrain.table[nloc].cost
                if possibilities:
                  nloc = random.choice(possibilities)
                  self.units[nloc] = enemy
                  del self.units[enemy.loc]
                  enemy.move(nloc)
                  return
            self.ai = -1
        while self.ai == -1:
        #for i in range(0, 2):
          if self.mouse.clicked(0):
            if self.mouse.pos[0] > 600 and self.mouse.pos[1] > 450:
              for unit in self.units.values():
                unit.reset()
              self.clearSelection()
              self.ai = 0
              break
            if self.selected == loc:
              self.clearSelection()
            elif self.selected is None and loc in self.units:
              self.selected = loc
              self.terrain.select(loc)
            elif loc in self.units and self.units[self.selected].side == 0 and self.units[loc].side == 1:
              if sum(abs(i-j) for (i,j) in zip(self.selected, loc)) != self.units[self.selected].range: break
              if self.units[self.selected].attacked: break
              self.result = (self.units[self.selected], self.units[loc])
              self.units[self.selected].movement = 0
              self.units[self.selected].attacked = True
              self.clearSelection()
              return self.result
            elif loc in self.units:
              self.clearSelection()
              self.selected = loc
              self.terrain.select(loc)
            elif self.selected and self.units[self.selected].side == 0 and loc in self.terrain.table and self.terrain.table[loc].over[1]:
              self.units[self.selected].move(loc)
              self.units[loc] = self.units[self.selected]
              del self.units[self.selected]
              self.clearSelection()
          break
        self.terrain.update()
        self.unitsr.update()
      finally:
        # eat queue becuase why not
        for event in pygame.event.get():
          if event.type == QUIT:
            raise Exception("Quitting")
    elif result:
      self.result[1].damage()
    else:
      self.result[0].damage()
  def snap(self, pos):
    return tuple(i - (i % j) for (i, j) in zip(pos, self.div))
  def loc(self, pos):
    return tuple(i // j for (i, j) in zip(pos, self.div))
  def pos(self, loc):
    return tuple(i * j for (i,j) in zip(loc, self.div))
  def draw(self, **kwargs):
    self.screen.blit(self.background, (0,0))
    self.terrain.draw(self.screen)
    self.unitsr.draw(self.screen)
    self.terrain.overlay(self.screen)
    if self.selected:
      font = pygame.font.Font(None, 36)
      sunit = self.units[self.selected]
      text = font.render(sunit.name, 1, (255,255,255))
      self.screen.blit(text, (610,100))
      text = font.render("Health : %d / %d" % (sunit.health, sunit.total_health), 1, (255,255,255))
      self.screen.blit(text, (610,140))
      text = font.render("Move : %d / %d" % (max(sunit.movement,0), sunit.total_movement), 1, (255,255,255))
      self.screen.blit(text, (610,180))
      text = font.render("Range : %d" % sunit.range, 1, (255,255,255))
      self.screen.blit(text, (610,220))
    self.endr.draw(self.screen)
    
  

