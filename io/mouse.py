class Mouse(object):
  def __init__(self):
    self.down    = set()
    self.clicked = set()
    self.pos = None
  def tick(self, pos):
    self.pos = pos
    self.clicked = set()
  def press(self, button):
    self.down.add(button)
  def release(self, button):
    self.down.remove(button)
    self.clicked.add(button)
  def handleClick(self, button):
    contained = button in self.clicked
    self.clicked.remove(button)
    return contained
