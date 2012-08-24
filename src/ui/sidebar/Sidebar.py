from Vector import *
import App
import Sprite

class Panel:
   def __init__(self, text, headerId):
      self.titleSprite = Sprite.Sprite("team-display-" + str(headerId))
      self.titleText = Sprite.Text(text, bold=True, align="center")

   def setPosition(self, position):
      self.titleSprite.setPosition(position)
      self.titleText.setPosition(vectorAdd(position, (0, -5)))

class Sidebar:
   def __init__(self, x):
      self.x = x
      self.background = Sprite.Sprite("sidebar", position=(x, 0))

      self.panels = []

   def layoutPanels(self):
      y = App.ui.windowCenter[1] - 50

      for panel in self.panels:
         panel.setPosition((self.x, y))
         y -= (panel.height() + 50)

   def addPanel(self, panel):
      self.panels.append(panel)

      self.layoutPanels()
