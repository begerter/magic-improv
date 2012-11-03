import pygame

class Transfer():
    def __init__(self, screen, comment, nextThing):
        self.screen = screen
        self.next = nextThing
        self.comment = comment
        self.font = pygame.font.SysFont(None,50)
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.counter = 0
        self.increment = 30

    def draw(self, **kwargs):
        self.background.fill((0,0,0))
        if self.counter < self.increment:
            text = self.font.render("3", True, (255,255,255))
        elif self.counter < self.increment*2:
            text = self.font.render("2", True, (255,255,255))
        elif self.counter < self.increment*3:
            text = self.font.render("1", True, (255,255,255))
        else:
            text = self.font.render(self.comment, True, (255,255,255))
        textRect = text.get_rect()
        self.background.blit(text, (textRect[0]+375, textRect[1]+300, \
                                    textRect[2], textRect[3]))
        self.screen.blit(self.background,(0,0))

    def update(self, **kwargs):
        self.counter += 1
        if self.counter > self.increment*4:
            return self.next
        
