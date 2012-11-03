import pygame

class Mouse(object):
  def __init__(self):
    self.last = None
    self.curr = None
  def tick(self):
    self.pos  = pygame.mouse.get_pos()
    self.last = self.curr
    self.curr = pygame.mouse.get_pressed()
  def clicked(self, button):
    if not self.last: return
    return self.curr[button] and not self.last[button]
  def clear(self):
    self.curr = None
