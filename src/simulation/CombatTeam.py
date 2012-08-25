import App
import imp
import Misc
import math
import Ship
import random
from Vector import *

nextTeamId = 0

class BasicCombatTeam:
   def __init__(self, name):
      self.shipsInFtl = []
      self.shipsInWorld = []
      self.ships = []

      self.name = name

      global nextTeamId
      self.id = nextTeamId
      nextTeamId += 1

      App.world.onUpdate += self.handleWorldUpdate

   def __eq__(self, rhs):
      return self is rhs

   def destroy(self):
      App.world.onUpdate -= self.handleWorldUpdate

   def activeShips(self):
      return self.shipsInWorld

   def addShip(self, ship):
      ship.onDestroy += self.handleShipDestroyed
      self.ships.append(ship)

   def handleWorldUpdate(self, world):
      if len(self.shipsInFtl) > 0 and world.randomValue(0, 20) == 0:
         self.jumpNextShip()

   def jumpNextShip(self):
      ship = self.shipsInFtl.pop()

      ship.position = self.randomPosition()
      ship.rotation = App.world.randomValue(0, 1000) * (math.pi / 1000.0)
      ship.velocity = ( App.world.randomValue(-6.0, 6.0) , App.world.randomValue(-6.0, 6.0) )

      self.shipsInWorld.append(ship)
      App.world.addObject(ship)

   # Destroyed
   def handleShipDestroyed(self, ship):
      self.shipsInWorld.remove(ship)


class CombatTeam(BasicCombatTeam):
   def __init__(self, fleet):
      BasicCombatTeam.__init__(self, fleet.name)

      self.loadFleet(fleet)

      App.world.onUpdate += self.handleWorldUpdate

   # Setup
   def loadFleet(self, fleet):
      for definition in fleet.ships:
         for i in range(definition.count):
            ship = Ship.Ship(definition, 
                             (0, 0), 0, (0, 0), self)

            self.addShip(ship)
            self.shipsInFtl.append(ship)

      random.shuffle(self.shipsInFtl)

   # FTL
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
