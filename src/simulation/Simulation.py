
import sys
import imp
import math
import World
import Ship
from Vector import *
import Cache
import Timing
import random
import Misc

WORLD_SIZE = Misc.WEAPON_RANGE

class Simulation:
   def __init__(self, seed, fleets, existingShips=[]):
      self.fleets = fleets
      self.seed = seed

      self.world = World.World(seed)

      teamId = 0
      for ship in existingShips:
         ship.world = self.world
         self.world.prepareObject(ship)
         self.world.addObject(ship)

      if len(existingShips) > 0:
         teamId = 1

      for fleet in fleets:
         self.loadFleet(fleet, teamId)
         teamId += 1

      random.shuffle(self.world.shipsToJump)

   def complete(self):
      if len(self.world.shipsToJump) > 0:
         return False

      teams = []
      for o in self.world.all:
         if not o.combatTeam in teams:
            teams.append(o.combatTeam)

         if len(teams) > 1:
            return False

      return True

   def loadFleet(self, fleet, fleetId):
      for definition in fleet.ships:
         for i in range(definition.count):
            position = self.randomPosition()
            rotation = self.world.randomValue(0, 1000) * (math.pi / 1000.0)
            velocity = ( self.world.randomValue(-6.0, 6.0) , self.world.randomValue(-6.0, 6.0) )

            autopilot = self.loadAutopilot(definition.autopilot)

            ship = Ship.Ship(definition.name, definition.design, autopilot, position, rotation, velocity, self.world, fleetId)
            self.world.addToHyperspace(ship)

   def loadAutopilot(self, autopilotName):
      return imp.load_source(autopilotName, "./src/playerdata/autopilot/%s.py" % (autopilotName,)).Autopilot

   def randomPosition(self):
      while True:
         newPosition = (self.world.randomValue(-WORLD_SIZE, WORLD_SIZE), self.world.randomValue(-WORLD_SIZE, WORLD_SIZE))
         
         minDistance = 999999999
         for obj in self.world.all:
            distance = vectorMagnitude(vectorOffset( obj.position, newPosition))
            
            if distance < minDistance:
               minDistance = distance
         
         if minDistance > Misc.WEAPON_RANGE:
            return newPosition

   @Timing.timedFunction
   def tick(self):
      Cache.clear()
      self.world.simulate()


