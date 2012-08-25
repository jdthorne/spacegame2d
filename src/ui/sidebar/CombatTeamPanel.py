
from Vector import *
from Scalar import *

import App
import Sidebar
import Sprite

class ShipPanelItem(Sidebar.Item):
   def __init__(self, ship):
      Sidebar.Item.__init__(self)

      ship.onUpdate += self.handleUpdate
      ship.onDestroy += self.handleUpdate
      self.ship = ship

      self.deflector = Sprite.Sprite("ship-deflector", layer=Sprite.sidebarGraphicsLayer)
      self.ok = Sprite.Sprite("ship-ok", layer=Sprite.sidebarGraphicsUpperLayer)
      self.damage = Sprite.Sprite("ship-damage", layer=Sprite.sidebarGraphicsUpperLayer)

   def destroy(self):
      self.ship.onUpdate -= self.handleUpdate
      self.ship.onDestroy -= self.handleUpdate

      self.deflector.destroy()
      self.ok.destroy()
      self.damage.destroy()

      Sidebar.Item.destroy(self)

   def setPosition(self, position):
      Sidebar.Item.setPosition(self, position)

      self.handleUpdate(self.ship)

   def handleUpdate(self, ship):
      if not ship.inWorld:
         if not ship.wasDestroyed:
            self.statusText.setAlpha(0.2)
            self.statusText.setText("in ftl...")
         else:
            self.statusText.setText("")

         self.nameText.setText("")

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
      if not ship.hasTakenDamage:
         self.ok.setPosition(vectorAdd(self.position, (120 - 6, 0)))
         self.damage.setPosition(vectorAdd(self.position, (120 + 6, 0)))
      else:
         self.ok.setPosition(vectorAdd(self.position, (120 + 6, 0)))
         self.damage.setPosition(vectorAdd(self.position, (120 - 6, 0)))

class CombatTeamPanel(Sidebar.Panel):
   def __init__(self, team):
      Sidebar.Panel.__init__(self, team.name, team.id)

      App.world.onCombatTeamRemoved += self.handleTeamRemoved

      self.team = team
      self.loadShips()

   def loadShips(self):
      for ship in self.team.ships:
         item = ShipPanelItem(ship)
         self.items.append(item)

   def handleTeamRemoved(self, world, team):
      if not (team is self.team):
         return

      self.destroy()
