from .unit import Unit
class Mullet(Unit):
  def __init__(self, **kwargs):
    super(Mullet, self).__init__(image="mulletlord.png",**kwargs)
    self.side = 1
    self.name = "Mullet Lord"