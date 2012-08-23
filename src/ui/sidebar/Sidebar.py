import Sprite
import Frame

from Scalar import *
from Vector import *

class Item:
   def __init__(self, title, subtitle="", icon=None):
      self.title = title
      self.subtitle = subtitle
      self.selected = False
      self.icon = icon

   def draw(self, x, yDelta):
      y = self.y + yDelta

      if self.icon == None:
         bold = True
         offset = 0

      else:
         bold = False
         offset = 30

      if self.selected:
         white = (255,255,255,255)

         Sprite.draw("ship-highlight-0", position=(x, y), hud=True)
         Sprite.drawText(self.title, position=(x - 110 + offset, y), bold=bold, color=white)
         Sprite.drawText(self.subtitle, position=(x - 20, y), bold=False, color=white)

      else:
         Sprite.draw("ship-display", position=(x, y), hud=True)
         Sprite.drawText(self.title, position=(x - 110 + offset, y), bold=bold)
         Sprite.drawText(self.subtitle, position=(x - 20, y), bold=False)

   def layout(self, y):
      self.y = y
      return y - 30

   def isHit(self, y):
      return (abs(y - self.y) < 15)

class Panel(Frame.Frame):
   def __init__(self, title, colorId, onItemSelected=None):
      self.title = title
      self.colorId = colorId
      self.items = []
      self.onItemSelected = onItemSelected

   def draw(self, x, yDelta):
      y = self.top + yDelta

      Sprite.draw("team-display-%s" % (self.colorId,), position=(x, y - 3), hud=True)
      Sprite.drawText(self.title, position=(x, y - 5), bold=True, align="center")
      y -= 35

      for item in self.items:
         y = item.draw(x, yDelta)

   def handleMouseDown(self, x, y):
      if y > self.top or y < self.bottom:
         return

      selectedItem = None
      for item in self.items:
         item.selected = item.isHit(y)

         if item.selected:
            selectedItem = item

      if self.onItemSelected != None:
         self.onItemSelected(selectedItem)

   def clearSelection(self):
      for item in self.items:
         item.selected = False

      if self.onItemSelected != None:
         self.onItemSelected(None)      

   def layout(self, y):
      self.top = y
      y -= 35

      for item in self.items:
         y = item.layout(y)

      self.bottom = y
      y -= 25

      return y

class Sidebar:
   def __init__(self, xShown, xHidden):
      self.x = xHidden
      self.y = (720/2)

      self.xTarget = xHidden
      self.xShown = xShown
      self.xHidden = xHidden

      self.panels = []

      self.isolate = False
      self.isolatedPanel = None
      self.isolateDistance = 0

   def show(self):
      self.xTarget = self.xShown
   def hide(self):
      self.xTarget = self.xHidden

   def tick(self, dt):
      if self.x != self.xTarget:
         self.x = scalarMix(0.6, self.x, self.xTarget)

         if abs(self.x - self.xTarget) < 5:
            self.x = self.xTarget

      if self.isolate and self.isolateDistance < 1000:
         self.isolateDistance += 20 * dt
         self.isolateDistance *= 1.25
      elif (not self.isolate) and (self.isolateDistance > 0):
         self.isolateDistance -= 20 * dt
         self.isolateDistance /= 1.25

         if self.isolateDistance < 10:
            self.isolateDistance = 0

   def draw(self):
      Sprite.draw("sidebar", position=(self.x, self.y), hud=True)

      yDelta = self.isolateDistance
      for panel in self.panels:
         if panel is self.isolatedPanel:
            panel.draw(self.x, 0)
            yDelta = -yDelta
            continue

         panel.draw(self.x, yDelta)

   def handleMouseDown(self, x, y):
      if abs(x - self.x) >= 120:
         return

      for panel in self.panels:
         panel.handleMouseDown(x, y)

   def layout(self):
      y = 720 - 30
      for panel in self.panels:
         y = panel.layout(y)

   def isolatePanel(self, panel):
      self.isolate = True
      self.isolateDistance = 0
      self.isolatedPanel = panel

   def cancelIsolation(self):
      self.isolate = False