from .unit import Unit
class Dude(Unit):
  def __init__(self, **kwargs):
    super(Dude, self).__init__(image="dude.png", **kwargs)
    self.side = 0
    self.name = "Duuudddde"