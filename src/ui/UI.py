
import App
import Timing
import pyglet
import Sprite
import Event
import Sidebar

from Vector import *

class UI:
   def __init__(self):
      self.windowSize = (1280, 720)
      self.windowCenter = vectorScale(self.windowSize, 0.5)

      self.batch = pyglet.graphics.Batch()
      self.batchText = pyglet.graphics.Batch()
      self.currentDisplay = None

      self.onTick = Event.Event(self)

   def setup(self):
      pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
      pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
      window = pyglet.window.Window(width=self.windowSize[0], height=self.windowSize[1])
      window.on_draw = self.draw
      window.on_mouse_motion = self.handleMouseMotion
      window.on_mouse_press = self.handleMouseDown
      self.window = window

      self.background = Sprite.Sprite("background", position=(0, 0))

      self.right = Sidebar.Sidebar(self.windowCenter[0] - 120)

   def start(self):
      fpsDisplay = pyglet.clock.ClockDisplay()
         
      pyglet.clock.set_fps_limit(30.0)
      pyglet.clock.schedule_interval(self.tick, 1/30.0)

      self.fpsDisplay = fpsDisplay
      pyglet.app.run()

   def display(self, display):
      self.currentDisplay = display

   def tick(self, dt):
      App.world.simulate()

      self.onTick(dt)

   @Timing.timedFunction
   def draw(self):
      self.window.clear()
      self.batch.draw()
      self.batchText.draw()
      self.fpsDisplay.draw()

   def handleMouseMotion(self, x, y, dx, dy):
      pass

   def handleMouseDown(self, x, y, button, modifier):
      pass


