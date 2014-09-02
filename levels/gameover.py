import pyglet
from pyglet.window.key import ENTER, BACKSPACE

from .levels import Level

class GameOver(Level):
  def __init__(self, window):
    self.text = 'Enter Initials: '
    self.welcome = pyglet.text.Label('Game\nOver', x=200, y=window.height-200,
                                    width=window.width//2,
                                    font_size=40, multiline=True)
    self.initials = pyglet.text.Label(self.text, x=200, y=window.height-400,
                                    font_size=20)
    super(GameOver, self).__init__(window)


  def hi_score(self, user, score):
    with open("scores.txt", "a") as fp:
      fp.write("%s: %s\n" % (user, round(float(score), 2)))

  def draw(self):
    self.window.clear()
    self.welcome.draw()
    self.initials.draw()

  def key(self, symbol, mod):
    """Let user enter 3 characters for high score list."""
    if symbol == ENTER:
      user = self.initials.text[len(self.text):]
      self.hi_score(user, str(self.messages.get("score", 0)))
      self.container.level = 0
    elif symbol == BACKSPACE:
      self.initials.text = self.initials.text[:-1]
    elif len(self.initials.text) < len(self.text) + 3:
      try:
        self.initials.text += chr(symbol)
      except:
        pass

