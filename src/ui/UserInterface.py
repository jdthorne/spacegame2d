
import pyglet
import Sprite
from Vector import *
import Timing

windowSize = (1280, 720)
halfWindowSize = vectorScale(windowSize, 0.5)

class UserInterface:
   def display(self, toDisplay):
      self.currentDisplay = toDisplay

   def start(self):
      pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
      pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
      window = pyglet.window.Window(width=windowSize[0], height=windowSize[1])
      fpsDisplay = pyglet.clock.ClockDisplay()
         
      @window.event
      def on_draw():
         self.draw()
      @window.event
      def on_mouse_motion(x, y, dx, dy):
         self.handleMouseMotion(x, y, dx, dy)

      pyglet.clock.set_fps_limit(30.0)
      pyglet.clock.schedule_interval(self.tick, 1/30.0)

      self.window = window
      self.fpsDisplay = fpsDisplay
      pyglet.app.run()

   def tick(self, dt):
      self.currentDisplay.tick(dt)

      if self.currentDisplay.complete():
         pyglet.app.exit()

   @Timing.timedFunction
   def draw(self):
      self.window.clear()

      Sprite.freeAll()
      self.currentDisplay.draw()
      Sprite.drawBatch()

      self.fpsDisplay.draw()

   def handleMouseMotion(self, x, y, dx, dy):
      self.currentDisplay.handleMouseMotion(x, y, dx, dy)
