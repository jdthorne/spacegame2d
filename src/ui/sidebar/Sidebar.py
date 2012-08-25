from Vector import *
import App
import Sprite
import Event
import SmoothedValue

class Item:
   def __init__(self, name="", status="", right=""):
      self.selected = False
      self.background = Sprite.Sprite("ship-display", layer=Sprite.sidebarPanelLayer)

      self.nameText = Sprite.Text(name, bold=True)
      self.statusText = Sprite.Text(status)
      self.rightText = Sprite.Text(right, align="right")

   def setPosition(self, position):
      self.position = position

      self.background.setPosition(position)
      self.nameText.setPosition(vectorAdd(position, (-110, 0)))
      self.statusText.setPosition(vectorAdd(position, (-40, 0)))
      self.rightText.setPosition(vectorAdd(position, (110, 0)))

   def setSelected(self, selected):
      if self.selected == selected:
         return

      self.selected = selected

      if selected:
         self.background.setImage("ship-highlight-0")
         self.nameText.setColor( (1, 1, 1) )
         self.statusText.setColor( (1, 1, 1) )
         self.rightText.setColor( (1, 1, 1) )
      else:
         self.background.setImage("ship-display")
         self.nameText.setColor( (0, 0, 0) )
         self.statusText.setColor( (0, 0, 0) )
         self.rightText.setColor( (0, 0, 0) )

   def handleMouseDown(self, x, y, button, modifier):
      if abs(y - self.position[1]) >= 11:
         return

      self.setSelected(True)

class Panel:
   def __init__(self, text, headerId):
      self.titleSprite = Sprite.Sprite("team-display-" + str(headerId), layer=Sprite.sidebarPanelLayer)
      self.titleText = Sprite.Text(text, bold=True, align="center")

      self.items = []

   def setPosition(self, position):
      self.position = position
      self.top = position[1]
      self.bottom = position[1] - self.height()

      self.titleSprite.setPosition(position)
      self.titleText.setPosition(vectorAdd(position, (0, -3)))

      position = vectorAdd(position, (0, -28))
      for item in self.items:
         item.setPosition(position)
         position = vectorAdd(position, (0, -22))

   def height(self):
      return 35 + (22 * len(self.items))

   def handleMouseDown(self, x, y, button, modifier):
      if y > self.top or y < self.bottom:
         return

      for item in self.items:
         item.handleMouseDown(x, y, button, modifier)


class Sidebar:
   def __init__(self, xHidden, xVisible):
      self.xHidden = xHidden
      self.xVisible = xVisible
      self.position = SmoothedValue.Vector((xHidden, 0), self.handlePositionUpdated)

      self.background = Sprite.Sprite("sidebar", layer=Sprite.sidebarBaseLayer)      
      self.onSelectionChanged = Event.Event(self)

      self.panels = []

   def show(self):
      self.position.set((self.xVisible, 0))

   def hide(self):
      self.position.set((self.xHidden, 0))

   def handlePositionUpdated(self, value, position):
      self.background.setPosition(position)
      self.layoutPanels()

   def layoutPanels(self):
      x = self.position()[0]
      y = App.ui.windowCenter[1] - 50

      for panel in self.panels:
         panel.setPosition((x, y))
         y -= (panel.height() + 50)

   def addPanel(self, panel):
      self.panels.append(panel)

      self.layoutPanels()

   def deselectAll(self):
      for panel in self.panels:
         for item in panel.items:
            item.setSelected(False)

   def handleMouseDown(self, x, y, button, modifier):
      if abs(self.position()[0] - x) >= 120:
         return

      selection = self.selection()
      self.deselectAll()

      for panel in self.panels:
         panel.handleMouseDown(x, y, button, modifier)

      if self.selection() is not selection:
         self.onSelectionChanged(self.selection())

   def selection(self):
      for panel in self.panels:
         for item in panel.items:
            if item.selected:
               return item

      return None