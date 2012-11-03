import pygame
import minigame

class Manager:
    def __init__(self):
        #self.turns = turns()
        self.minigames = []
        self.current = minigame.Minigame()

    def draw(self, screen):
        self.current.draw(screen)

    def update(self):
        self.current.update()
        
