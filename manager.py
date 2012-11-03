import pygame
import minigame
from tbg.board import Board
from easywin import EasyWin
from missiles import Missiles
_TBG = "tbg"
_MINI = "mini"

class Manager:
    def __init__(self, screen, clock, **kwargs):
        #self.turns = turns()
        self.status = _MINI
        self.minigames = []
        self.board = Board(screen=screen, clock=clock)
        self.missiles = Missiles(screen=screen,clock=clock)
        self.easywin = EasyWin(screen)
        self.current = self.missiles

    def draw(self, screen):
        self.current.draw()

    def update(self):
        catcher = self.current.update()
        if self.status == _MINI and catcher != None:
            self.current = self.board
            self.status = _TBG
            # pass along results to board somehow?
        
