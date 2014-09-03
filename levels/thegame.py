import pyglet
from pyglet.window.key import ENTER

from .levels import Level
from .game_piece import Problem
from .drawing import rectangle

class TheGame(Level):
  def __init__(self, window):
    self.user_answer = pyglet.text.Label('', x=10, y=window.height-30, font_size=20)
    self.score_text = pyglet.text.Label('0', x=window.width-100, y=window.height-30, font_size=20)
    self.score = 0
    self.game_piece = Problem(window)
    super(TheGame, self).__init__(window)


  def key(self, symbol, mod):
    self.game_piece.speed = self.score / 10 + 1
    num = set(range(ord("0"), ord("9") + 1))
    # If answer box, check to see if they were right
    if symbol == ENTER:
      score = self.game_piece.check(self.user_answer.text) # Get back time elapsed or None
      if score:
        # score is elapsed time on the answer. Give bonus on <2 seconds answers
        score = 2 - score
        if score < 0:
          score = 0
        self.score += 1 + score
        self.score_text.text = "%.02f" % self.score
      self.user_answer.text = ''
    elif symbol in num:
      self.user_answer.text += chr(symbol)

  def draw(self):
    self.window.clear()
    self.game_piece.draw()
    rectangle(0, self.window.height-40, 40, self.window.width)
    self.user_answer.draw()
    self.score_text.draw()

  def clock(self, dt):
    self.game_piece.update(dt)
    if self.game_piece.fail():
      self.container.next()
      # Pass score to next "level"
      self.container.current.msg(score=self.score)

  def reset(self):
    self.game_piece.reset()
    self.score_text.text = ""
    self.score = 0
