import pygame
from pygame.locals import *
import manager as man
import sys

# load resources

# initialize
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.mouse.set_visible(1)
clock = pygame.time.Clock()
manager = man.Manager(screen=screen, clock=clock)

# setup display
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250,0,0))
screen.blit(background, (0,0))


#main loop
while True:
    clock.tick(60)
    
    manager.update()
    manager.draw(screen)

    pygame.display.flip()

