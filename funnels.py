import pyglet

from game_piece import Problem

window = pyglet.window.Window(fullscreen=True)
user_answer = pyglet.text.Label('  ', x=10, y=window.height-30, font_size=20)
game_piece = Problem(window)    

pyglet.clock.schedule(game_piece.update)

@window.event
def on_key_press(symbol, modifiers):
  if ord("0") <= symbol <= ord("9"):
    user_answer.text = chr(symbol)
    game_piece.check(user_answer.text)
    
@window.event
def on_draw():
  window.clear()
  game_piece.draw()
  user_answer.draw()

pyglet.app.run()
