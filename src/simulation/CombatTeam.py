import App
import imp
import Misc
import math
import Ship
from Vector import *

nextTeamId = 0

class CombatTeam:
   def __init__(self, fleet):
      self.shipsInFtl = []
      self.shipsInWorld = []
      self.ships = []

      self.name = fleet.name
      self.loadFleet(fleet)

      global nextTeamId
      self.id = nextTeamId
      nextTeamId += 1

      App.world.onUpdate += self.handleWorldUpdate

   def __eq__(self, rhs):
      return self is rhs

   # Current Status
   def activeShips(self):
      return self.shipsInWorld

   # Setup
   def loadFleet(self, fleet):
      for definition in fleet.ships:
         for i in range(definition.count):
            autopilot = self.loadAutopilot(definition.autopilot)

            ship = Ship.Ship(definition.name, definition.design, autopilot, 
                             (0, 0), 0, (0, 0), App.world, self)

            ship.onDestroy += self.handleShipDestroyed

            self.shipsInFtl.append(ship)
            self.ships.append(ship)

   def loadAutopilot(self, autopilotName):
      return imp.load_source(autopilotName, "./src/playerdata/autopilot/%s.py" % (autopilotName,)).Autopilot

   # Destroyed
   def handleShipDestroyed(self, ship):
      self.shipsInWorld.remove(ship)

   # FTL
   def handleWorldUpdate(self, world):
      if len(self.shipsInFtl) > 0 and world.randomValue(0, 10) == 0:
         self.jumpNextShip()

   def jumpNextShip(self):
      ship = self.shipsInFtl.pop()

      ship.position = self.randomPosition()
      ship.rotation = App.world.randomValue(0, 1000) * (math.pi / 1000.0)
      ship.velocity = ( App.world.randomValue(-6.0, 6.0) , App.world.randomValue(-6.0, 6.0) )

      self.shipsInWorld.append(ship)
      App.world.addObject(ship)

   def randomPosition(self):
      for i in range(1, 5):
         newPosition = (App.world.randomValue(-App.world.size, App.world.size), App.world.randomValue(-App.world.size, App.world.size))
         
         minDistance = 999999999
         for obj in App.world.all:
            distance = vectorMagnitude(vectorOffset( obj.position, newPosition))
            
            if distance < minDistance:
               minDistance = distance
         
         if minDistance > (Misc.WEAPON_RANGE / i):
            return newPosition

      return newPosition
