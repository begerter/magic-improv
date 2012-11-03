import pygame
import minigame
from missiles import Missiles
from easywin import EasyWin
from tbg.board import Board
from whackamullet import WhackAMullet
from freeze import Freeze
import random

_TBG = "tbg"
_MINI = "mini"

class Manager:
    def __init__(self, screen, clock, **kwargs):
        #self.turns = turns()
        self.screen = screen
        self.status = _TBG
        self.minigames = []
        self.board = Board(screen=screen, clock=clock)
        self.minigames.append(Missiles(screen=screen,clock=clock))
        self.minigames.append(WhackAMullet(screen=screen,clock=clock))
        self.minigames.append(Freeze(screen=screen,clock=clock))
        self.minigames.append(EasyWin(screen))
        self.current = self.board
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
                self.current = self.minigames[random.randint(0,len(self.minigames)-1)]
                self.status = _MINI
                self.currWait = self.wait
        else:
            #clear queue
            self.currWait -= 1
            pygame.event.get()
        
