import pyglet

from pyglet.window.key import ENTER, SPACE, BACKSPACE

from game_piece import Problem
from levels import Levels, Level

window = pyglet.window.Window()#fullscreen=True)

class TheGame(Level):
  def __init__(self):
    self.user_answer = pyglet.text.Label('', x=10, y=window.height-30, font_size=20)
    self.score_text = pyglet.text.Label('0', x=window.width-100, y=window.height-30, font_size=20)
    self.score = 0
    self.game_piece = Problem(window)
    super(TheGame, self).__init__()


  def key(self, symbol, mod):
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
    window.clear()
    self.game_piece.draw()
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

class IntroScreen(Level):
  def __init__(self):
    self.welcome = pyglet.text.Label('WELCOME\n\tTO\nCLAIRE', x=100, y=window.height-80,
                                    width=window.width//2,
                                    font_size=40, multiline=True)
    
    scores = self.get_scores()
    print scores
    self.scores = pyglet.text.Label("".join(scores), x=100, y=window.height-280,
                                    width=int(window.width * .8),
                                    font_size=30, multiline=True)
    super(IntroScreen, self).__init__()

  def get_scores(self):
    with open("scores.txt") as fp:
      lines = fp.readlines()
    lines = sorted(lines, reverse=True, key=lambda l: float(l.split(': ')[-1]))
    return ["{}. {}".format(i, line) for i, line in enumerate(lines[:5], 1)]

  def key(self, symbol, mod):
    if symbol == SPACE:
      self.container.next()

  def draw(self):
    window.clear()
    self.welcome.draw()
    self.scores.draw()

class GameOver(Level):
  def __init__(self):
    self.text = 'Enter Initials: '
    self.welcome = pyglet.text.Label('Game\nOver', x=200, y=window.height-200,
                                    width=window.width//2,
                                    font_size=40, multiline=True)
    self.initials = pyglet.text.Label(self.text, x=200, y=window.height-400,
                                    font_size=20)
    super(GameOver, self).__init__()


  def hi_score(self, user, score):
    with open("scores.txt", "a") as fp:
      fp.write("%s: %s\n" % (user, round(score, 2)))

  def draw(self):
    window.clear()
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


levels = Levels([IntroScreen(), TheGame(), GameOver()])
pyglet.clock.schedule(levels.clock)

@window.event
def on_key_press(symbol, modifiers):
  levels.key(symbol, modifiers)

@window.event
def on_draw():
  levels.draw()

pyglet.app.run()
