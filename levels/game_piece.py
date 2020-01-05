import random
import pyglet

# some constants for state of problem
FALLING, EXPLODING = 1, 2
# some colors
RED = (255, 0, 0, 255)


class Problem(object):
  """Wraps problem generation (what math problem are we solving) and behavior. (1 hit? 2 hits? Special speedup?)

  """
  animation = pyglet.image.load_animation('resources/explosion.gif')
  explosion_snd = pyglet.resource.media('resources/explosion.wav', streaming=False)
  boop_snd = pyglet.resource.media('resources/boop.wav', streaming=False)
  explosion = pyglet.sprite.Sprite(animation)

  def __init__(self, window):
    self.window = window
    self.time = 0
    self.speed = 1
    self.high_score = 0
    self.problem = pyglet.text.Label('', x=100, y=self.window.height, font_size=20, color=RED)
    self.answer = ""
    self.value = 1
    self.reset()


  def generate_problem(self):
    answer = random.choice(range(2, 10))
    a = answer - random.choice(range(1, answer))
    b = answer - a
    problem = "%s + %s" % (a, b)
    self.answer = str(answer)
    self.problem.text = problem
    self.time = 0

  def update(self, dt):
    # drop the position of the problem text
    self.time += dt
    self.problem.y -= self.speed

  def reset(self, dt=None, level=0):
    self.state = FALLING
    # pick a random value of x between 0 and width of window (- some margins)
    self.problem.x = random.choice(range(50, self.window.width - 50))
    self.problem.y = self.window.height
    self.generate_problem()

  def check(self, answer):
    self.boop_snd.play()
    if answer == self.answer:
      self.state = EXPLODING
      self.explosion_snd.play()
      self.explosion._frame_index = 0 # this is probably bad and wrong.
      pyglet.clock.schedule_once(self.reset, 1)
      return self.time

  def fail(self, y=0):
    if self.problem.y <= y and self.state == FALLING:
      return True

  def draw(self):
    if self.state == FALLING:
      self.problem.draw()
    else:
      self.explosion.x, self.explosion.y = self.problem.x, self.problem.y
      self.explosion.draw()
