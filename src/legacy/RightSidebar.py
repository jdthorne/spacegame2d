import Sprite
import Sidebar

X_SHOWN = (1280 - 120)
X_HIDDEN = (1280 + 120)

class RightSidebar(Sidebar.Sidebar):
   def __init__(self):
      Sidebar.Sidebar.__init__(self, X_SHOWN, X_HIDDEN)

      self.titlePanel = Sidebar.Panel("Fleet Designer", "plain")
      self.panels.append(self.titlePanel)

      self.fleetPanels = []

   def clear(self, title):
      self.titlePanel.title = title

      for panel in self.fleetPanels:
         self.panels.remove(panel)

      self.fleetPanels = []

      self.onShipSelected = None

   def displayFleet(self, fleet, ships, teamId):
      fleetPanel = Sidebar.Panel(fleet.name, teamId, onItemSelected=self.handleShipItemSelected)

      for ship in ships:
         item = Sidebar.Item(ship.name, ship.status)
         item.ship = ship

         fleetPanel.items.append(item)

      self.fleetPanels.append(fleetPanel)
      self.panels.append(fleetPanel)

   def handleShipItemSelected(self, shipItem):
      if self.onShipSelected != None:
         if shipItem == None:
            self.onShipSelected(None)
         else:
            self.onShipSelected(shipItem.ship)

