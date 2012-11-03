import pygame
import minigame
from tbg.board import Board
from easywin import EasyWin

_TBG = "tbg"
_MINI = "mini"

class Manager:
    def __init__(self, screen, clock, **kwargs):
        #self.turns = turns()
        self.screen = screen
        self.status = _MINI
        self.minigames = []
        self.board = Board(screen=screen, clock=clock)
        self.easywin = EasyWin(screen)
        self.current = self.easywin
        self.catcher = None
        self.wait = 7
        self.currWait = 0

    def draw(self, screen):
        self.current.draw()

    def update(self):
        if self.currWait == 0:
            self.catcher = self.current.update(result=self.catcher)
            if self.status == _MINI and self.catcher != None:
                print "switching to tbg"
                self.current.reset()
                self.current = self.board
                self.status = _TBG
                self.currWait = self.wait
            elif self.status == _TBG and self.catcher != None:
                print "switching to mini"
                self.easywin = EasyWin(self.screen)
                self.current = self.easywin
                self.status = _MINI
                self.currWait = self.wait
        else:
            self.currWait -= 1
            pygame.event.get()
        
