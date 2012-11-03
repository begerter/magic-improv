import pygame
from pygame.locals import *
from sys import exit

class Board(object):
  def __init__(self, screen, clock):
    self.screen = screen
    self.clock  = clock
  def update(self):
    for event in pygame.event.get():
      if event.type == QUIT:
        exit(0)
  def draw(self):
    background = pygame.Surface(self.screen.get_size())
    background = background.convert()
    background.fill((250,0,0))
    self.screen.blit(background, (0,0))