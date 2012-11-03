import pygame
from pygame.locals import *
import os
loaded = {}

COLORS = ((0,0,250), (0,250,0), (250,250,0))

class Base(pygame.sprite.Sprite):
  def __init__(self, loc, cost, board, image, **kwargs):
    super(Base, self).__init__(**kwargs)
    self.cost = cost
    self.board = board
    if image not in loaded:
      loaded[image] = pygame.image.load(os.path.join("assets", image))
    self.image = loaded[image]
    self.rect = pygame.rect.Rect(board.pos(loc), self.image.get_size())
    self.loc = loc
    self.left = 0
    self.clear()
  def clear(self):
    self.over = [False, False, False]
  def enter(self, num):
    self.over[num] = True
  def select(self):
    self.enter(0)
  def movable(self, left):
    self.enter(1)
    self.left = left
  def attackable(self):
    self.enter(2)
  def overlay(self, screen):
    for i,v in enumerate(self.over):
      if v: break
    else: return
    if i == 1 and self.loc in self.board.units: return
    color = COLORS[i]
    select = pygame.Surface(tuple(i-1 for i in self.board.div))
    select.convert()
    select.fill(color)
    screen.blit(select, self.board.pos(self.loc), special_flags = BLEND_ADD)
    return i
