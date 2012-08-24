
from Vector import *
from Scalar import *

import Sidebar
import Sprite

class ShipPanelItem(Sidebar.Item):
   def __init__(self, ship):
      Sidebar.Item.__init__(self)

      ship.onUpdate += self.handleUpdate
      ship.onDestroy += self.handleUpdate
      self.ship = ship

      self.deflector = Sprite.Sprite("ship-deflector")
      self.ok = Sprite.Sprite("ship-ok")
      self.damage = Sprite.Sprite("ship-damage")

   def setPosition(self, position):
      Sidebar.Item.setPosition(self, position)

      self.handleUpdate(self.ship)

   def handleUpdate(self, ship):
      if not ship.inWorld:
         self.nameText.setText("")
         self.statusText.setText("")

         self.deflector.setPosition(vectorAdd(self.position, (500, 0)))
         self.ok.setPosition(vectorAdd(self.position, (500, 0)))
         self.damage.setPosition(vectorAdd(self.position, (500, 0)))
         return

      # Name
      self.nameText.setText(ship.name)

      # Status
      importance, status = ship.status
      self.statusText.setAlpha(importance)
      self.statusText.setText(status.lower())

      # Deflector
      deflectorWidthModifier = 1.0 - (1.0 / ship.maxDeflectorPower)
      deflectorWidth = 4 + (deflectorWidthModifier * (50 - 4))

      deflectorPower = scalarBound(0, ship.availableDeflectorPower / ship.maxDeflectorPower, 1.0)
      deflectorPosition = int(deflectorPower * deflectorWidth)

      self.deflector.setPosition(vectorAdd(self.position, (120 - 12 + 25 - deflectorPosition, 0)))

      # Structural Integrity
      if not ship.damaged:
         self.ok.setPosition(vectorAdd(self.position, (120 - 6, 0)))
         self.damage.setPosition(vectorAdd(self.position, (120 + 6, 0)))
      else:
         self.ok.setPosition(vectorAdd(self.position, (120 + 6, 0)))
         self.damage.setPosition(vectorAdd(self.position, (120 - 6, 0)))


class CombatTeamPanel(Sidebar.Panel):
   def __init__(self, team):
      Sidebar.Panel.__init__(self, team.name, team.id)

      self.team = team
      self.loadShips()

   def loadShips(self):
      self.items = []

      for ship in self.team.ships:
         item = ShipPanelItem(ship)
         self.items.append(item)

