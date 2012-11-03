import pygame
from pygame.locals import *

# load resources

# initialize
pygame.init()
screen = pygame.display.set_mode((468, 60))
pygame.mouse.set_visible(0)
clock = pygame.time.Clock()

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
            break
