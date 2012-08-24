
from Vector import *
from Scalar import *

import Sidebar
import Sprite

class FleetPanel(Sidebar.Panel):
   def __init__(self, fleet):
      Sidebar.Panel.__init__(self, fleet.name, "plain")

      self.fleet = fleet
      