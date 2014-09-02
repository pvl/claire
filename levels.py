class Level(object):
  """Provide object that handles draw, clock, and key events."""
  
  def __init__(self):
    self.container = None

  def reset(self):
    """Called when a level is loaded."""
    pass
    
  def register_container(self, container):
    """Maintain a handle on parent so we can do game operations like advance to the next level.
    """
    self.container = container

    
  def clock(self, dt):
    pass

  def key(self, symbol, mod):
    pass

  def draw(self):
    pass
    
    
class Levels(object):
  """Utility class to store several Level objects and pick which one is handling drawing and events."""

  def __init__(self, levels_list, current_level=0):
    self._level = current_level
    self._levels = levels_list
    self._current = self._levels[current_level]
    self._current.reset()
    for level in self._levels:
      level.register_container(self)

  @property
  def level(self):
    return self._level
    
  @level.setter
  def level(self, val):
    self._current = self._levels[val]
    self._level = val
    self._current.reset()

  def clock(self, dt):
    self._current.clock(dt)

  def key(self, symbol, mod):
    self._current.key(symbol, mod)

  def draw(self):
    self._current.draw()
    
  def next(self):
    self.level += 1

  def prev(self):
    self.level -= 1
    
