import pygame

# 
class Minigame(pygame.sprite.Group):
    def __init__(self, screen):
        pygame.sprite.Group.__init__(self)
        self.screen = screen

    def draw(self):
        pygame.sprite.Group.draw(self, self.screen)

    def update(self):
        for event in pygame.event.get():
            #do whatever you want to do
            print "hi"
    
