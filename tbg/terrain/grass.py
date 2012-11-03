import pygame
from pygame.locals import *
import os
from .base import Base

class Grass(Base):
  def __init__(self, **kwargs):
    super(Grass, self).__init__(cost=1,image=os.path.join("terrain","grass.png"),**kwargs)
