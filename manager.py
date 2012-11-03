import pygame
import minigame
from missiles import Missiles
from easywin import EasyWin
from tbg.board import Board
from whackamullet import WhackAMullet
from freeze import Freeze
from clickclack import ClickClack
from platformer import Game as Platformer
from transfer import Transfer
import random
from slides import Slideshow
_INTRO = "intro"
_TBG = "tbg"
_MINI = "mini"
_TRANSFER = "transfer"

class Manager:
    def __init__(self, screen, clock, **kwargs):
        #self.turns = turns()
        self.screen = screen
        self.status = _INTRO
        self.minigames = []
        self.board = Board(screen=screen, clock=clock)
        self.intro = Slideshow(screen=screen,slides=((1800000,"andrewdrewanelephant.png"),))
        self.minigames.append((Missiles(screen=screen,clock=clock),["Dodge"]))
        self.minigames.append((WhackAMullet(screen=screen,clock=clock), ["Kill"]))
        self.minigames.append((Freeze(screen=screen,clock=clock), ["Dodge", "Kill", "Jump", "Type"]))
        self.minigames.append((Platformer(clock=clock,screen=screen), ["Jump"]))
        #self.minigames.append(EasyWin(screen))
        self.minigames.append((ClickClack(screen), ["Type"]))
        self.current = self.intro
        self.catcher = None
        self.wait = 7
        self.currWait = 0

    def draw(self, screen):
        self.current.draw()

    def update(self):
        if self.status != _TRANSFER:
            self.catcher = self.current.update(result=self.catcher)
            if self.status == _MINI and self.catcher != None:
                print "switching to tbg"
                self.current.reset()
                self.current = self.board
                self.status = _TBG
                self.currWait = self.wait
            elif self.status == _TBG and self.catcher != None:
                print "switching to transfer"
                self.easywin = EasyWin(self.screen)
                self.status = _TRANSFER
                select = self.minigames[random.randint(0,len(self.minigames)-1)]
                self.current = Transfer(self.screen,select[1][random.randint(0,len(select[1])-1)],select[0])
                #self.current = self.minigames[random.randint(0,len(self.minigames)-1)]
                #self.status = _MINI
                self.currWait = self.wait
            elif self.status == _INTRO and self.catcher != None:
              self.catcher = None
              self.current.reset()
              self.current = self.board
              self.status = _TBG
              self.currWait = self.wait 
        else:
            #clear queue
            #self.currWait -= 1
            result = self.current.update()
            pygame.event.get()
            if result != None:
                print "switching to mini"
                self.current = result
                self.status = _MINI

        
