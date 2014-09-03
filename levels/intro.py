import pyglet
from pyglet.window.key import SPACE

from .levels import Level


class IntroScreen(Level):
  def __init__(self, window):
    self.welcome = pyglet.text.Label('WELCOME\n\tTO\nCLAIRE', x=100, y=window.height-80,
                                    width=window.width//2,
                                    font_size=40, multiline=True)

    scores = self.get_scores()
    self.scores = pyglet.text.Label("".join(scores), x=100, y=window.height-280,
                                    width=int(window.width * .8),
                                    font_size=30, multiline=True)
    super(IntroScreen, self).__init__(window)

  def reset(self):
    scores = self.get_scores()
    self.scores.text = "".join(scores)

  def get_scores(self):
    with open("scores.txt") as fp:
      lines = fp.readlines()
    lines = sorted(lines, reverse=True, key=lambda l: float(l.split(': ')[-1]))
    return ["#{} - {}".format(i, line) for i, line in enumerate(lines[:5], 1)]

  def key(self, symbol, mod):
    if symbol == SPACE:
      self.container.next()

  def draw(self):
    self.window.clear()
    self.welcome.draw()
    self.scores.draw()
