import pygame
import minigame
import random

class ClickClack(minigame.Minigame):
    class word:
        def __init__(self, pword):
            self.word = pword
            self.x = random.randint(100,700)
            self.y = 0

        def match(self, s):
            return s == self.word
        
        def draw(self, bg):
            
    def __init__(self, screen):
        minigame.Minigame.__init__(self, screen)
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.words = []
        self.result = None

    def draw(self):
        self.background.fill((0,0,255))
        self.screen.blit(self.background, (0,0))

    def update(self):
        return self.result
