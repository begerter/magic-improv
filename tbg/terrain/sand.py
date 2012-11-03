import pygame
from pygame.locals import *
import os
from .base import Base

class Sand(Base):
  def __init__(self, **kwargs):
    super(Sand, self).__init__(cost=2,image=os.path.join("terrain","sand.png"),**kwargs)
