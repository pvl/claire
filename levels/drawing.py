import pyglet

def rectangle(left_x, bottom_y, height, width):
  pyglet.gl.glColor4f(1.0,0,0,1.0)
  tl = (left_x, bottom_y + height)
  tr = (left_x + width, bottom_y + height)
  bl = (left_x, bottom_y)
  br = (left_x + width, bottom_y)
  pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                               [0, 1, 2, 0, 2, 3],
                               ('v2i', tl + tr + br + bl)
                               )
  
