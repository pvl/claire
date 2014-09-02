import pyglet

from pyglet.window.key import ENTER, SPACE

from game_piece import Problem
from levels import Levels, Level

window = pyglet.window.Window()#fullscreen=True)

class TheGame(Level):
  def __init__(self):
    self.user_answer = pyglet.text.Label('', x=10, y=window.height-30, font_size=20)
    self.score_text = pyglet.text.Label('0', x=window.width-100, y=window.height-30, font_size=20)
    self.score = 0
    self.game_piece = Problem(window)
    

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
  
  def reset(self):
    self.game_piece.reset()
    self.score_text.text = ""
    self.score = 0

class IntroScreen(Level):
  def __init__(self):
    self.welcome = pyglet.text.Label('WELCOME\n\tTO\nCLAIRE', x=100, y=window.height-200,
                                    width=window.width//2,
                                    font_size=60, multiline=True)
  def key(self, symbol, mod):
    if symbol == SPACE:
      self.container.next()
      
  def draw(self):
    window.clear()
    self.welcome.draw()

class GameOver(Level):
  def __init__(self):
    self.welcome = pyglet.text.Label('Game\nOver', x=200, y=window.height-200,
                                    width=window.width//2,
                                    font_size=40, multiline=True)

  def draw(self):
    window.clear()
    self.welcome.draw()

  def key(self, symbol, mod):
    if symbol == SPACE:
      self.container.prev()
    
    
levels = Levels([IntroScreen(), TheGame(), GameOver()])
pyglet.clock.schedule(levels.clock)

@window.event
def on_key_press(symbol, modifiers):
  levels.key(symbol, modifiers)
    
@window.event
def on_draw():
  levels.draw()

pyglet.app.run()
