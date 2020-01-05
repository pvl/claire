class Level(object):
  """Provide object that handles draw, clock, and key events."""

  def __init__(self, window):
    self.container = None
    self.window = window
    self.messages = {}

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

  def msg(self, **kwargs):
    self.messages.update(kwargs)


class Levels(object):
  """Utility class to store several Level objects and pick which one is handling drawing and events."""

  def __init__(self, levels_list, current_level=0):
    self._level = current_level
    self._levels = levels_list
    self.current = self._levels[current_level]
    self.current.reset()
    for level in self._levels:
      level.register_container(self)

  @property
  def level(self):
    return self._level

  @level.setter
  def level(self, val):
    self.current = self._levels[val]
    self._level = val
    self.current.reset()

  def clock(self, dt):
    self.current.clock(dt)

  def key(self, symbol, mod):
    self.current.key(symbol, mod)

  def draw(self):
    self.current.draw()

  def advance(self):
    self.level += 1
    return self

  @property
  def prev(self):
    self._level -= 1
    return self

  def next(self):
    return self.advance()
