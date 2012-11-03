import minigame
import pygame

class EasyWin(minigame.Minigame):
    def __init__(self, screen):
        minigame.Minigame.__init__(self, screen)
        self.result = None
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()

    def draw(self, **kwargs):
        self.background.fill((0,255,0))
        pygame.draw.rect(self.background, (0,0,255), pygame.Rect(50,50,100,100))
        self.screen.blit(self.background, (0,0))

    def reset(self):
        self.result = None
        
    def update(self, **kwargs):

        # check for clicks
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] < 150 and pos[0] > 50 and pos[1] < 150 and pos[1] > 50:
                    self.result = True
                else:
                    self.result = False
                break

        # if there was a click, we are done
        if self.result != None:
            status = self.result
            print "Done: ", status
            return status
