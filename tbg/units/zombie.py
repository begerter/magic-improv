from .unit import Unit
class Zombie(Unit):
  def __init__(self, **kwargs):
    super(Zombie, self).__init__(image="mulletMook.png",move=1,**kwargs)
    self.side = 1
    self.name = "Mook"
