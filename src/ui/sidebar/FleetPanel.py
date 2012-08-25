
from Vector import *
from Scalar import *

import Sidebar
import Sprite

class FleetPanelItem(Sidebar.Item):
   def __init__(self, shipDef):
      Sidebar.Item.__init__(self)

      self.shipDef = shipDef

      self.nameText.setText(shipDef.name)
      self.statusText.setText(shipDef.autopilot)
      self.rightText.setText("x%d" % (shipDef.count,))

class FleetPanel(Sidebar.Panel):
   def __init__(self, fleet):
      Sidebar.Panel.__init__(self, fleet.name, "plain")

      self.fleet = fleet

      for shipDef in fleet.ships:
         self.items.append(FleetPanelItem(shipDef))
