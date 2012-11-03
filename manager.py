import pygame
import minigame
from tbg.board import Board

class Manager:
    def __init__(self):
        #self.turns = turns()
        self.minigames = []
        self.board = Board(screen=screen, clock=clock)
        self.current = self.board

    def draw(self, screen):
        self.current.draw()

    def update(self):
        self.current.update()
        
