import minigame

def load_image(name, colorkey=None):
    fullname = os.path.join('assets', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__int__(self)
        self.image,self.rect = load_image('dude.png', -1)
        self.moveUp = false
        self.moveDown = false
        self.moveRight = false
        self.moveLeft = false
        self.moveRate = 4
    def update():
        for event in pygame.event.get():
            if event.type = QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.moveRight = False
                    self.moveLeft = True
                if event.key == K_RIGHT:
                    self.moveRight = True
                    self.moveLeft = False
                if event.key == K_UP:
                    self.moveUp = True
                    self.moveDown = False
                if event.key == K_DOWN:
                    self.moveUp = True
                    self.moveDown = False
            if self.moveLeft and playerRect.left > 0:
                playerRect.self.move_ip(-1 * self.moveRate, 0)
            if self.moveRight and playerRect.right < screen.width():
                playerRect.self.move_ip(self.moveRate, 0)
            if self.moveUp and playerRect.top > 0:
                playerRect.self.move_ip(0, -1 * self.moveRate)
            if self.moveDown and playerRect.bottom < screen.height():
                playerRect.self.move_ip(0, self.moveRate)
class runner(minigame.Minigame):
    def __init__(self,screen):
        minigame.Minigame.init()
        self.player = Player()
        self.clock = pygame.time.Clock()
        self.allsprites = pygame.sprite.RenderPlain(player)

    def update():
        self.clock.tick(60)
        self.allsprites.update()
        screen.blit(background, (0,0))
        allsprites.draw(screen)
        pygame.display.flip()
    
 
