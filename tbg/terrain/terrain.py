import pygame
from pygame.locals import *
import os
import heapq
from .base import Base

class Terrain(object):
  def __init__(self, board, **kwargs):
    super(Terrain, self).__init__(**kwargs)
    self.table = dict( ((x,y), Base(loc=(x,y),cost=1,board=board,image="base_terrain.png"))
                      for x in range(10) for y in range(10) )
    self.renderer = pygame.sprite.RenderPlain(tuple(self.table.values()))
    self.board    = board
  def clear(self):
    for t in self.table.values(): t.clear()
  def select(self, loc):
    self.table[loc].select()
    if loc in self.board.units:
      side = self.board.units[loc].side
      move = self.board.units[loc].movement
      heap = [ (0, loc) ]
      while heap:
        m, loc = heapq.heappop(heap)
        if loc not in self.table: continue
        if self.table[loc].over[1]: continue
        if loc in self.board.units and self.board.units[loc].side != side: continue
        self.table[loc].movable(m)
        if m < move:
          m += self.table[loc].cost
          for i,j in ((1,0),(0,1),(-1,0),(0,-1)):
            heapq.heappush(heap, (m, (loc[0]+i,loc[1]+j)))
  def update(self):
    self.renderer.update()
  def draw(self, screen):
    self.renderer.draw(screen)
  def overlay(self, screen):
    for t in self.table.values():
      t.overlay(screen)
    