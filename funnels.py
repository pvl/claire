import pyglet

from levels import GameOver, IntroScreen, TheGame
from levels.levels import Levels

window = pyglet.window.Window()#fullscreen=True)

levels = Levels([IntroScreen(window), TheGame(window), GameOver(window)])
pyglet.clock.schedule(levels.clock)

@window.event
def on_key_press(symbol, modifiers):
  levels.key(symbol, modifiers)

@window.event
def on_draw():
  levels.draw()

pyglet.app.run()
