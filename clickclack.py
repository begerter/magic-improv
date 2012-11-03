import pygame, os
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
            return self.y > 500
        
        def draw(self, bg):
            bg.blit(self.text, (self.textRect[0]+self.x,self.textRect[1]+self.y,
                                self.textRect[2], self.textRect[3]))
            
    def __init__(self, screen):
        minigame.Minigame.__init__(self, screen)
        self.font = pygame.font.SysFont(None, 20)
        self.font2 = pygame.font.SysFont(None,42)
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        self.screen.blit(self.background, (0,0))
        self.back = pygame.image.load(os.path.join('assets','mullettypebg.png'))
        self.backRect = self.back.get_rect()
        pygame.display.flip()
        self.words = []
        self.current = ""
        self.result = None
        self.baseSpawn = 5
        self.toSpawn = self.baseSpawn
        self.score = 0
        self.killed = 0
        self.wordlist = ["mullet", "mullet", "mullet", "mullet", "help", "mullet",\
                         "save me", "mullet", "mullet"]
        try:
            self.noprotag = pygame.image.load(os.path.join('assets','noprotag.png'))
            self.nomullet = pygame.image.load(os.path.join('assets', 'nomullet.png'))
            self.yesprotag = pygame.image.load(os.path.join('assets', 'yesprotag.png'))
            self.yesmullet = pygame.image.load(os.path.join('assets', 'yesmullet.png'))
            self.noprotag = self.noprotag.convert()
            self.nomullet = self.nomullet.convert()
            self.yesprotag = self.yesprotag.convert()
            self.yesmullet = self.yesmullet.convert()
        except pygame.error, message:
            print "Cannot load image"
            raise SystemExit, message

    def draw(self, **kwargs):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.back, self.backRect)
        for i in self.words:
            i.draw(self.screen)

        text = self.font2.render(">"+self.current, True, (255,0,0))
        textRect = text.get_rect()
        self.screen.blit(text, (textRect[0]+350, textRect[1]+400,\
                                    textRect[2], textRect[3]))

        self.drawScore(self.screen)
        self.drawFailure(self.screen)
        pygame.display.flip()

    def drawScore(self, bg):
        counter = self.score
        for i in xrange(3): #you have 3 lives
            if counter > 0:
                counter -= 1
                pic = self.noprotag
            else:
                pic = self.yesprotag
            picRect = pic.get_rect()
            bg.blit(pic, (picRect[0]+25, picRect[1]+100*i,\
                          picRect[2], picRect[3]))

    def drawFailure(self, bg):
        counter = self.killed
        for i in xrange(5): #you have to kill 5 things
            if counter > 0:
                counter -= 1
                pic = self.nomullet
            else:
                pic = self.yesmullet
            picRect = pic.get_rect()
            bg.blit(pic, (picRect[0]+725, picRect[1]+100*i,\
                          picRect[2], picRect[3]))

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
        self.killed = 0
        self.words = []
        
    def update(self, **kwargs):
        remove = False
        clear = False
        self.spawn()

        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key == pygame.K_RETURN:
                clear = True
            if event.key == pygame.K_BACKSPACE:
                self.current = self.current[:-1]
            else:
                self.current += event.unicode
        
        for i in self.words:
            if i.match(self.current):
                i.toDelete = True
                remove = True
                self.killed += 1
            elif i.update():
                i.ToDelete = True
                self.score += 1
        if remove:
            self.current = ""
        self.words = [i for i in self.words if not i.toDelete]

        if clear:
            self.current = ""
        self.result = self.won()   
        return self.result
