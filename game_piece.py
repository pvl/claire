import random
import pyglet

# some constants for state of problem
FALLING, EXPLODING = 1, 2
# some colors
RED = (255, 0, 0, 255)


class Problem(object):
  def __init__(self, window):
    self.window = window
    animation = pyglet.image.load_animation('resources/explosion.gif')
    self.explosion = pyglet.sprite.Sprite(animation)
    self.explosion_snd = pyglet.resource.media('resources/explosion.wav', streaming=False)
    self.boop_snd = pyglet.resource.media('resources/boop.wav', streaming=False)
    self.problem = pyglet.text.Label('', x=100, y=self.window.height, font_size=20, color=RED)
    self.answer = ""
    self.reset()
    
  
  def generate_problem(self):
    answer = random.choice(range(2, 10))
    a = answer - random.choice(range(1, answer))
    b = answer - a
    problem = "%s + %s" % (a, b)
    self.answer = str(answer)
    self.problem.text = problem

  def update(self, dt):
    # drop the position of the problem text
    self.problem.y -= 1

  def reset(self, dt=None):
    self.state = FALLING
    # pick a random value of x between 0 and width of window (- some margins)
    self.problem.x = random.choice(xrange(50, self.window.width - 50))
    self.problem.y = self.window.height
    self.generate_problem()

  def check(self, answer):
    self.boop_snd.play()
    if answer == self.answer:
      self.state = EXPLODING
      self.explosion_snd.play()
      self.explosion._frame_index = 0 # this is probably bad and wrong.
      pyglet.clock.schedule_once(self.reset, 1)
      
  def draw(self):
    if self.state == FALLING:
      self.problem.draw()
    else:
      self.explosion.x, self.explosion.y = self.problem.x, self.problem.y
      self.explosion.draw()
