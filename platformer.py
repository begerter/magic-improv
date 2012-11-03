''' Platforming game for 2012 5C Hackathon

Based on public domain code written by
Richard Jones <richard@mechanicalcat.net>

'''

import pygame
import tmx
import minigame


class Enemy(pygame.sprite.Sprite):
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
    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('player-right.png')
        self.right_image = self.image
        self.left_image = pygame.image.load('player-left.png')
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        # is the player resting on a surface and able to jump?
        self.resting = False
        # player's velocity in the Y direction
        self.dy = 0
        # is the player dead?
        self.is_dead = False
        # movement in the X direction; postive is right, negative is left
        self.direction = 1

    def update(self, dt, game):
        # take a copy of the current position of the player before movement for
        # use in movement collision response
        last = self.rect.copy()

        # handle the player movement left/right keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 300 * dt
            self.image = self.left_image
            self.direction = -1
        if key[pygame.K_RIGHT]:
            self.rect.x += 300 * dt
            self.image = self.right_image
            self.direction = 1

        # if the player's allowed to let them jump with the spacebar; note that
        # wall-jumping could be allowed with an additional "touching a wall"
        # flag
        if self.resting and key[pygame.K_SPACE]:
            game.jump.play()
            # we jump by setting the player's velocity to something large going
            # up (positive Y is down the screen)
            self.dy = -500

        # add gravity on to the currect vertical speed
        self.dy = min(400, self.dy + 40)

        # now add the distance travelled for this update to the player position
        self.rect.y += self.dy * dt

        # collide the player with the map's blockers
        new = self.rect
        # reset the resting trigger; if we are at rest it'll be set again in the
        # loop; this prevents the player from being able to jump if they walk
        # off the edge of a platform
        self.resting = False
        # look up the tilemap triggers layer for all cells marked "blockers"
        for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
            # find the actual value of the blockers property
            blockers = cell['blockers']
            # now for each side set in the blocker check for collision; only
            # collide if we transition through the blocker side (to avoid
            # false-positives) and align the player with the side collided to
            # make things neater
            if 'l' in blockers and last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if 'r' in blockers and last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if 't' in blockers and last.bottom <= cell.top and new.bottom > cell.top:
                self.resting = True
                new.bottom = cell.top
                # reset the vertical speed if we land or hit the roof; this
                # avoids strange additional vertical speed if there's a
                # collision and the player then leaves the platform
                self.dy = 0
            if 'b' in blockers and last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.dy = 0

        # re-focus the tilemap viewport on the player's new position
        game.tilemap.set_focus(new.x, new.y)

class Game(minigame):
    def __init__(self, clock, screen):
        super.__init__(screen)
        self.clock = clock
        self.tilemap = tmx.load(assets/platformerMaps/map1.tmx)
        self.background = pygame.image.load('assets/platformerbg.png')
        pygame.mouse.set_visible(0)

        self.tilemap = tmx.load('map1.tmx', screen.get_size())

        # add a layer for our sprites controlled by the tilemap scrolling
        self.sprites = tmx.SpriteLayer()
        self.tilemap.layers.append(self.sprites)
        # fine the player start cell in the triggers layer
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        # use the "pixel" x and y coordinates for the player start
        self.player = Player((start_cell.px, start_cell.py), self.sprites)

        # add a separate layer for enemies so we can find them more easily later
        self.enemies = tmx.SpriteLayer()
        self.tilemap.layers.append(self.enemies)
        # add an enemy for each "enemy" trigger in the map
        for enemy in self.tilemap.layers['triggers'].find('enemy'):
            Enemy((enemy.px, enemy.py), self.enemies)


    def exit(self, bool):
        pygame.mouse.set_visible(1)
        #throw back to master
        #clear screen

    def update(self, dt):
        if self.player.won:
            return exit(True)
            
        if self.player.isDead:
            return exit(False)
    
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


        
def main:
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))

    game = Game(clock, screen)

    while done == None:
        dt = clock.tick(60)
        done = game.update(dt)
        game.draw()
