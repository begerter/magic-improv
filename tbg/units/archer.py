from .unit import Unit
class Archer(Unit):
  def __init__(self, **kwargs):
    super(Archer, self).__init__(image="bowdude.png",range=2,move=2,health=5,**kwargs)
    self.side = 0
    self.range = 2
    self.name = "Archer"
