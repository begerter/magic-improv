import pygame

# 
class Minigame(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def draw(self, screen):
        pygame.sprite.Group.draw(self, screen)

    def update(self):
        for event in pygame.event.get():
            #do whatever you want to do
            print "hi"
    
