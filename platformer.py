''' Platforming game for 2012 5C Hackathon

Based on public domain code written by
Richard Jones <richard@mechanicalcat.net>

'''

import pygame
import tmx
import minigame


class Enemy(pygame.sprite.Sprite)
    image = pygame.image.load('assets/enemy.jpg')
    def __init__(self, location, *groups):
        super(Enemy, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        #1 is forward, -1 is backward, enemies move back and forth
        self.direction = 1 
        
    def update(self, dt, game):
        self.rect.x += self.direction * 100 * dt
        
        #check collisions
        for cell in game.tilemap.layers['triggers'].collide(self.rect, 'reverse'):
            if self.direction > 0:
                self.rect.right = cell.left
            else:
                self.rect.left = cell.right
            self.direction *= -1
            break

        if self.rect.colliderect(game.player.rect):
            game.player.isDead = true


class Player(pygame.sprite.Sprite):
    #etc...

class Game(minigame):
    def __init__(self, clock, screen):
        super.__init__(screen)
        self.clock = clock
        self.tilemap = tmx.load(assets/plaformerMaps/map1.tmx)
        self.background = pygame.image.load('assets/platformerbg.png')
        pygame.mouse.set_visible(0)

        

    def exit(self, bool):
        pygame.mouse.set_visible(1)
        #throw back to master
        #clear screen

    def update(self):
        if self.player.won:
            exit(True)
            
        if self.player.isDead:
            exit(False)
    
        dt = clock.tick(30)
        
        self.tilemap.update(dt / 1000., self)
        player.update(dt, self)
        for enemy in enemies:
            enemy.update(dt, self)

        #draw()
        #is called by master

    def draw(self)
        screen.blit(background, (0,0))
        self.tilemap.draw(screen)
        pygame.display.flip()


        
