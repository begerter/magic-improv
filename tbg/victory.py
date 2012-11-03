class Win(Exception):
  def __init__(self, *args, **kwargs):
    super(Win,self).__init__(*args,**kwargs)
class Lose(Exception):
  def __init__(self, *args, **kwargs):
    super(Win,self).__init__(*args,**kwargs)
