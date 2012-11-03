import minigame, os

_red = (255,0,0)
_green = (0,255,0)
_yellow = (200,200,0)

class redlight(minigame.Minigame):
    class Competitor:
        def __init__(self, filename, start, ai):
            self.vel = 0
            self.start= start
            self.pos = self.start
            self.ai = ai
            try:
                self.img = pygame.image.load(os.path.join('assets',filename))
            except pygame.error, message:
                print 'Cannot load image:', filename
                raise SystemExit, message
            self.img = self.img.convert()
            self.rect = self.img.get_rect()
            
        def update(self, light):
            self.pos += self.vel
            if self.ai:
                if light == _green:
                    self.vel = 10
                if light == _yellow:
                    self.vel = 0
            if light == _red and self.vel != 0:
                reset()

        def won(self):
            return self.start > 700:

        def reset(self):
            self.pos = self.start
            self.vel = 0
            
    def __init__(self, screen):
        minigame.Minigame.__init__(self, screen)
        self.light = _red
        self.result = None
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()

    def draw(self):
        self.background.fill((0,255,0))
        draw_light()
        self.screen.blit(self.background, (0,0))

    def draw_light(self):
        pygame.draw.rect(self.background, self.light, pygame.Rect(375,0,50,50))
        
    def update(self):
        self.
