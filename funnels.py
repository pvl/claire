import pyglet
import argparse
from levels import GameOver, IntroScreen, TheGame
from levels.levels import Levels

def main(fullscreen):
  window = pyglet.window.Window(fullscreen=fullscreen)

  levels = Levels([IntroScreen(window), TheGame(window), GameOver(window)])
  pyglet.clock.schedule(levels.clock)

  @window.event
  def on_key_press(symbol, modifiers):
    levels.key(symbol, modifiers)

  @window.event
  def on_draw():
    levels.draw()

  pyglet.app.run()

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Arithemetic practice game.")
  parser.add_argument('--fullscreen', action="store_true", help='Turn on fullscreen. Defaults to True')
  parser.add_argument('--no-fullscreen', dest="fullscreen", action="store_false", help='Turn off fullscreen. Defaults to False')
  parser.set_defaults(fullscreen=True)
  results = parser.parse_args()
  main(results.fullscreen)
