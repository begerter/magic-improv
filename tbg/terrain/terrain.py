from __future__ import division
import pygame
from pygame.locals import *
import os
import heapq
from .base import Base
from .sand import Sand
from .grass import Grass
from .water import Water

TERRAIN = (
  Grass, Grass, Grass, Grass, Sand , Water, Water, Water, Water, Water,
  Grass, Grass, Grass, Grass, Sand , Water, Sand , Water, Water, Water,
  Grass, Grass, Grass, Grass, Sand , Water, Water, Water, Water, Water,
  Grass, Grass, Grass, Grass, Sand , Sand , Sand , Water, Water, Water,
  Grass, Grass, Grass, Grass, Sand , Sand , Sand , Sand , Sand , Sand ,
  Grass, Sand , Sand,  Sand , Grass, Sand , Sand , Sand , Sand , Sand ,
  Grass, Sand , Water, Sand , Grass, Grass, Grass, Sand , Sand , Sand ,
  Grass, Sand , Sand , Sand , Grass, Grass, Grass, Grass, Grass, Grass,
  Grass, Grass, Grass, Grass, Grass, Grass, Sand , Grass, Grass, Grass,
  Grass, Grass, Grass, Grass, Grass, Grass, Sand , Grass, Grass, Grass,
)

class Terrain(object):
  def __init__(self, board, **kwargs):
    super(Terrain, self).__init__(**kwargs)
    self.table = dict( ((i%10,i//10), type(loc=(i%10,i//10),board=board))
                      for (i, type) in enumerate(TERRAIN) )
    self.renderer = pygame.sprite.RenderPlain(tuple(self.table.values()))
    self.board    = board
  def clear(self):
    for t in self.table.values(): t.clear()
  def select(self, loc):
    self.table[loc].select()
    if loc in self.board.units:
      side = self.board.units[loc].side
      move = self.board.units[loc].movement
      urange = self.board.units[loc].range
      heap = [ (0, loc) ]
      while heap:
        m, loc = heapq.heappop(heap)
        if loc not in self.table: continue
        if self.table[loc].over[1]: continue
        if loc in self.board.units and self.board.units[loc].side != side: continue
        if self.table[loc].cost == -1: continue
        self.table[loc].movable(m)
        if m < move:
          m += self.table[loc].cost
          for i,j in ((1,0),(0,1),(-1,0),(0,-1)):
            heapq.heappush(heap, (m, (loc[0]+i,loc[1]+j)))
        for i in range(0,urange+1):
          j = urange - i
          for si, sj in ((1,1),(1,-1),(-1,1),(-1,-1)):
            try:
              self.table[(loc[0]+i*si,loc[1]+j*sj)].attackable()
            except KeyError:
              pass
  def update(self):
    self.renderer.update()
  def draw(self, screen):
    self.renderer.draw(screen)
  def overlay(self, screen):
    for t in self.table.values():
      t.overlay(screen)
    