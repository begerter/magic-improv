import pygame
import minigame
import random

class ClickClack(minigame.Minigame):
    class Word:
        def __init__(self, pword, font):
            self.word = pword
            self.x = random.randint(100,700)
            self.y = 0
            self.text = font.render(self.word, True, (255,255,255))
            self.textRect = self.text.get_rect()
            self.toDelete = False

        def match(self, s):
            return s == self.word

        def update(self):
            """ returns true if it needs to be dissappeared"""
            self.y += 2
            return self.y > 700
        
        def draw(self, bg):
            bg.blit(self.text, (self.textRect[0]+self.x,self.textRect[1]+self.y,
                                self.textRect[2], self.textRect[3]))
            
    def __init__(self, screen):
        minigame.Minigame.__init__(self, screen)
        self.font = pygame.font.SysFont(None, 20)
        self.font2 = pygame.font.SysFont(None,42)
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.words = []
        self.current = ""
        self.result = None
        self.baseSpawn = 5
        self.toSpawn = self.baseSpawn
        self.score = 0
        self.wordlist = ["mullet"]#, "bad", "blood", "terror", "sunglasses", "fight",\
                         #"death", "orange"]

    def draw(self, **kwargs):
        self.background.fill((0,0,255))
        for i in self.words:
            i.draw(self.background)

        text = self.font2.render(">"+self.current, True, (255,0,0))
        textRect = text.get_rect()
        self.background.blit(text, (textRect[0]+350, textRect[1]+400,\
                                    textRect[2], textRect[3]))
        
        self.screen.blit(self.background, (0,0))

    def won(self):
        if self.score > 3:
            return False
        if self.toSpawn == 0 and len(self.words) == 0:
            return True

    def spawn(self):
        if self.toSpawn > 0:
            r = random.randint(0,60)
            if r == 1:
                self.words.append(self.Word(self.wordlist[random.randint(0,len(self.wordlist)-1)],self.font))
                self.toSpawn -= 1

    def reset(self):
        self.score = 0
        self.toSpawn = self.baseSpawn
        
    def update(self, **kwargs):
        remove = False
        clear = False
        self.spawn()

        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key == pygame.K_RETURN:
                clear = True
            else:
                self.current += event.unicode
        
        for i in self.words:
            if i.match(self.current):
                i.toDelete = True
                remove = True
                break
        if remove:
            self.current = ""
        self.words = [i for i in self.words if (not i.toDelete) and (not i.update())]

        if clear:
            self.current = ""
        self.result = self.won()   
        return self.result
