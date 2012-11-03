from .unit import Unit
class Zombie(Unit):
  def __init__(self, **kwargs):
    super(Zombie, self).__init__(image="enemy.png",**kwargs)
    self.side = 1
