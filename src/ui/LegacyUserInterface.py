
import pyglet
import Sprite
from Vector import *
import Timing

import LeftSidebar
import RightSidebar

halfWindowSize = vectorScale(windowSize, 0.5)
viewWindowCenter = halfWindowSize

leftSidebar = LeftSidebar.LeftSidebar()
rightSidebar = RightSidebar.RightSidebar()

class UserInterface:
   def display(self, toDisplay):
      self.currentDisplay = toDisplay


