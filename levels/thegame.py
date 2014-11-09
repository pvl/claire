import pyglet
from pyglet.window.key import ENTER

from .levels import Level
from .game_piece import Problem
from .drawing import rectangle

class TheGame(Level):
  def __init__(self, window):
    self.user_answer = pyglet.text.Label('', x=10, y=window.height-30, font_size=20)
    self.score_text = pyglet.text.Label('0', x=window.width-100, y=window.height-30, font_size=20)
    self.difficulty_text = pyglet.text.Label('', x=window.width-200, y=window.height-300, font_size=20)
    self.score = 0
    self.difficulty_show = 0
    super(TheGame, self).__init__(window)
    self.game_piece = Problem(window)

  def key(self, symbol, mod):
    self.game_piece.speed = self.score / 10 + 1
    if 65457 <= symbol <= 65465:
        symbol -= 65408  # drop num pad to ascii 0-9 range
    num = set(range(ord("0"), ord("9") + 1))
    # If answer box, check to see if they were right
    if symbol == ENTER:
      score = self.game_piece.check(self.user_answer.text) # Get back time elapsed or None
      if score:
        # score is elapsed time on the answer. Give bonus on <2 seconds answers
        score = 2 - score
        if score < 0:
          score = 0
        self.score += self.game_piece.value + score
        self.score_text.text = "%.02f" % self.score
      self.user_answer.text = ''
    elif symbol in num:
      self.user_answer.text += chr(symbol)

  @property
  def difficulty(self):
    high_score = getattr(self, 'high_score', 0)
    return (high_score if high_score > self.score else self.score) / 10 + 1

  def draw(self):
    self.window.clear()
    if self.difficulty_show:
      self.difficulty_text.draw()
      self.difficulty_show -= 1
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
    print self.messages
    self.high_score = self.messages.get('high_score', 0)
    self.game_piece.reset(self.difficulty)
    self.score_text.text = ""
    self.difficulty_text.text = 'Difficulty: %s' % self.difficulty
    self.score = 0
    self.difficulty_show = 40
