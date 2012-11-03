import pygame
from pygame.locals import *
import manager as man

# load resources

# initialize
pygame.init()
screen = pygame.display.set_mode((468, 60))
pygame.mouse.set_visible(0)
clock = pygame.time.Clock()
manager = man.Manager()

# setup display
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250,0,0))
screen.blit(background, (0,0))


#main loop
while True:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            exit

    manager.update()
    manager.draw(screen)
