
import App
import Timing
import pyglet
import Sprite
import Event

from Vector import *

class UI:
   def __init__(self):
      self.windowSize = (1280, 720)
      self.windowCenter = vectorScale(self.windowSize, 0.5)

      self.batch = pyglet.graphics.Batch()
      self.currentDisplay = None

      self.onTick = Event.Event(self)

   def display(self, display):
      self.currentDisplay = display

   def start(self):
      pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
      pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
      window = pyglet.window.Window(width=self.windowSize[0], height=self.windowSize[1])
      fpsDisplay = pyglet.clock.ClockDisplay()
         
      window.on_draw = self.draw
      window.on_mouse_motion = self.handleMouseMotion
      window.on_mouse_press = self.handleMouseDown

      pyglet.clock.set_fps_limit(30.0)
      pyglet.clock.schedule_interval(self.tick, 1/30.0)

      self.background = Sprite.create("background")

      self.window = window
      self.fpsDisplay = fpsDisplay
      pyglet.app.run()

   def tick(self, dt):
      App.world.simulate()

      self.onTick(dt)

   @Timing.timedFunction
   def draw(self):
      self.window.clear()
      self.batch.draw()
      self.fpsDisplay.draw()

   def handleMouseMotion(self, x, y, dx, dy):
      pass

   def handleMouseDown(self, x, y, button, modifier):
      pass


