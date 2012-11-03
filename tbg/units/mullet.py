from .unit import Unit
from ..victory import Win
class Mullet(Unit):
  def __init__(self, **kwargs):
    super(Mullet, self).__init__(image="mulletlord.png",health=15,move=1,**kwargs)
    self.side = 1
    self.name = "Mullet Lord"
  def damage(self):
    super(Mullet, self).damage()
    if self.health <= 0:
      raise Win()
