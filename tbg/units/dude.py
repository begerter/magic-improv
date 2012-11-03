from .unit import Unit
class Dude(Unit):
  def __init__(self, **kwargs):
    super(Dude, self).__init__(image="andrewdrewanelephant.png", **kwargs)
    self.side = 0