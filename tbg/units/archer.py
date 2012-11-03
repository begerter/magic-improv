from .unit import Unit
class Archer(Unit):
  def __init__(self, **kwargs):
    super(Archer, self).__init__(image="bowdude.png", **kwargs)
    self.side = 0
    self.range = 2