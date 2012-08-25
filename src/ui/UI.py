
import App
import Timing
import pyglet
import Sprite
import Event
import Sidebar
import CombatTeamPanel

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
      window.on_mouse_drag = self.handleMouseDrag
      self.window = window

      self.background = Sprite.Sprite("background", position=(0, 0))

      self.left = Sidebar.Sidebar(-(self.windowCenter[0] + 120), -(self.windowCenter[0] - 120))
      self.right = Sidebar.Sidebar(+(self.windowCenter[0] + 120), +(self.windowCenter[0] - 120))

      self.right.show()

      App.world.onCombatTeamAdded += self.handleCombatTeamAdded

   def handleCombatTeamAdded(self, world, team):
      panel = CombatTeamPanel.CombatTeamPanel(team)
      self.right.addPanel(panel)

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
      x, y = vectorAdd( (x, y), vectorScale(self.windowCenter, -1) )
      if self.currentDisplay != None:
         self.currentDisplay.handleMouseMoved(x, y, dx, dy)

   def handleMouseDown(self, x, y, button, modifier):
      x, y = vectorAdd( (x, y), vectorScale(self.windowCenter, -1) )
      self.left.handleMouseDown(x, y, button, modifier)
      self.right.handleMouseDown(x, y, button, modifier)

      if self.currentDisplay != None:
         self.currentDisplay.handleMouseDown(x, y, button, modifier)

   def handleMouseDrag(self, x, y, dx, dy, button, modifier):
      self.handleMouseMotion(x, y, dx, dy)
      self.handleMouseDown(x, y, button, modifier)