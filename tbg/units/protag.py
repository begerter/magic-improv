from .unit import Unit
from ..victory import Lose
class Protag(Unit):
  def __init__(self, **kwargs):
    super(Protag, self).__init__(image="protag.png", **kwargs)
    self.side = 0
    self.name = "You"
  def damage(self):
    super(Protag, self).damage()
    if self.health <= 0:
      raise Lose()
