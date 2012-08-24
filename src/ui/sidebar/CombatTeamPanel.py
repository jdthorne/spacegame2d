
from Vector import *
from Scalar import *

import Sidebar
import Sprite

class ShipPanelItem:
   def __init__(self, ship):
      ship.onUpdate += self.handleUpdate
      ship.onDestroy += self.handleUpdate
      self.ship = ship

      self.background = Sprite.Sprite("ship-display")

      self.nameText = Sprite.Text("", bold=True)
      self.statusText = Sprite.Text("")
      self.deflector = Sprite.Sprite("ship-deflector")
      self.ok = Sprite.Sprite("ship-ok")
      self.damage = Sprite.Sprite("ship-damage")

   def setPosition(self, position):
      self.position = position

      self.background.setPosition(position)
      self.nameText.setPosition(vectorAdd(position, (-110, 0)))
      self.statusText.setPosition(vectorAdd(position, (-40, 0)))

      self.updateDeflectorPosition()

   def handleUpdate(self, ship):
      self.updateDeflectorPosition()

      if not ship.inWorld:
         self.nameText.setText("")
         self.statusText.setText("")
         return

      self.nameText.setText(ship.name)

      importance, status = ship.status
      self.statusText.setAlpha(importance)
      self.statusText.setText(status.lower())

   def updateDeflectorPosition(self):
      ship = self.ship 

      if not ship.inWorld:
         self.deflector.setPosition(vectorAdd(self.position, (500, 0)))
         self.ok.setPosition(vectorAdd(self.position, (500, 0)))
         self.damage.setPosition(vectorAdd(self.position, (500, 0)))
         return

      deflectorWidthModifier = 1.0 - (1.0 / ship.maxDeflectorPower)
      deflectorWidth = 4 + (deflectorWidthModifier * (50 - 4))

      deflectorPower = scalarBound(0, ship.availableDeflectorPower / ship.maxDeflectorPower, 1.0)
      deflectorPosition = int(deflectorPower * deflectorWidth)

      self.deflector.setPosition(vectorAdd(self.position, (120 - 12 + 25 - deflectorPosition, 0)))

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

   def height(self):
      return 35 + (22 * len(self.items))

   def loadShips(self):
      self.items = []

      for ship in self.team.ships:
         item = ShipPanelItem(ship)
         self.items.append(item)

   def setPosition(self, position):
      Sidebar.Panel.setPosition(self, position)

      position = vectorAdd(position, (0, -28))
      for item in self.items:
         item.setPosition(position)

         position = vectorAdd(position, (0, -22))
