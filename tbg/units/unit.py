import pygame
import os
loaded = {}

class Unit(pygame.sprite.Sprite):
  def __init__(self, board, image, loc, **kwargs):
    super(Unit, self).__init__(**kwargs)
    self.board = board
    if image not in loaded:
      loaded[image] = pygame.image.load(os.path.join("assets", image))
    self.image = loaded[image]
    self.rect = pygame.rect.Rect((0,0), self.image.get_size())
    self.move(loc)
    self.movement = 3
    self.range    = 1
  def move(self, loc):
    self.rect.topleft = self.board.pos(loc)
    self.loc = loc

