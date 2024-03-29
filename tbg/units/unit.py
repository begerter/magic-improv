import pygame
import os
loaded = {}

class Unit(pygame.sprite.Sprite):
  def __init__(self, board, image, loc, health=10, move=3, range=1, **kwargs):
    super(Unit, self).__init__(**kwargs)
    self.board = board
    if image not in loaded:
      loaded[image] = pygame.image.load(os.path.join("assets", image))
    self.image = loaded[image]
    self.rect = pygame.rect.Rect((0,0), self.image.get_size())
    self.total_movement = move
    self.range    = range
    self.total_health = health
    self.health   = self.total_health
    self.reset()
    self.move(loc)
  def move(self, loc):
    self.rect.topleft = self.board.pos(loc)
    self.loc = loc
    self.movement -= self.board.terrain.table[loc].left
  def reset(self):
    self.movement = self.total_movement
    self.attacked = False
  def damage(self):
    self.health -= 1
    if not self.health:
      self.rect.topleft = self.board.pos((10,10))
      del self.board.units[self.loc]

