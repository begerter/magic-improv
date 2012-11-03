import pygame
from pygame.locals import *
import os
from .base import Base

class Water(Base):
  def __init__(self, **kwargs):
    super(Water, self).__init__(cost=-1,image=os.path.join("terrain","water.png"),**kwargs)
