from .unit import Unit
class Protag(Unit):
  def __init__(self, **kwargs):
    super(Protag, self).__init__(image="protag.png", **kwargs)
    self.side = 0
    self.name = "You"