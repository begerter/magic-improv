import pygame
from pygame.locals import *
from sys import exit

WIDTH = 0
HEIGHT= 1

class Board(object):
  def __init__(self, screen, clock, div=(80,60), **kwargs):
    self.screen = screen
    self.clock  = clock
    self.genBackground(div)
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
    for event in pygame.event.get():
      if event.type == QUIT:
        exit(0)
  def draw(self, **kwargs):
    self.screen.blit(self.background, (0,0))
   