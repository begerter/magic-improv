import pygame
from pygame.locals import *
import sys
# load resources

# initialize
pygame.init()
screen = pygame.display.set_mode((468, 120))
pygame.mouse.set_visible(0)
clock = pygame.time.Clock()

# setup display
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250,0,0))
screen.blit(background, (0,0))

from tbg.board import Board
board = Board(screen, clock)
#main loop
while True:
  clock.tick(60)
  board.update()
  board.draw()

