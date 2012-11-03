import pygame
from minigame import Minigame
import os
from tbg.io.mouse import Mouse

class SingleSprite(pygame.sprite.Sprite):
  def __init__(self, name):
    super(SingleSprite,self).__init__()
    self.image = pygame.image.load(os.path.join(os.path.join("assets","slides"),name))
    self.rect = pygame.rect.Rect((0,0), self.image.get_size())
    self.group = pygame.sprite.RenderPlain((self,))
  def draw(self, screen):
    self.group.draw(screen)

class Slideshow(Minigame):
  def __init__(self, screen, slides):
    self.screen = screen
    self.slides = tuple((time,SingleSprite(name)) for (time,name) in slides)
    self.reset()
    self.mouse = Mouse()
  def draw(self):
    for time, slide in self.slides[self.curr:]:
      if self.time < time:
        slide.draw(self.screen)
        return
  def reset(self):
    self.time = 0
    self.curr = 0
  def update(self,**kwargs):
    for event in pygame.event.get():
      pass
    self.mouse.tick()
    self.time += 1
    if self.slides[-1][0] < self.time or self.mouse.last and any(a and b for (a,b) in zip(self.mouse.last,self.mouse.curr)):
      return True
