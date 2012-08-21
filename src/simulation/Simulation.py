
import sys
import imp
import math
import World
import Ship
from Vector import *
import Cache
import Timing

worldSize = 4500

class Simulation:
   def __init__(self, fleets, seed):
      self.fleets = fleets
      self.seed = seed

      self.world = World.World(seed)

      i = 0
      for fleet in fleets:
         self.loadFleet(fleet, i)
         i += 1

   def complete(self):
      teams = []
      for o in self.world.all:
         if not o.combatTeam in teams:
            teams.append(o.combatTeam)

         if len(teams) > 1:
            return False

      return True

   def loadFleet(self, fleet, fleetId):
      targetPath = "src/playerdata/%s/" % (fleet,)

      path = sys.path
      sys.path.append(targetPath)
      fleetModule = imp.load_source(fleet, targetPath + "Fleet.py")
      autopilotModule = imp.load_source(fleet, targetPath + "Autopilot.py")
      sys.path = path

      fleet = fleetModule.fleet()
      autopilot = autopilotModule.Autopilot 

      for ship in fleet:
         self.loadShip(ship, autopilot, fleetId)

   def loadShip(self, design, autopilot, fleetId):
      position = self.randomPosition()
      rotation = self.world.randomValue(0, 1000) * (math.pi / 1000.0)

      ship = Ship.Ship(design, autopilot, position, rotation, self.world, fleetId)
      self.world.addObject(ship)

   def randomPosition(self):
      while True:
         newPosition = (self.world.randomValue(-worldSize, worldSize), self.world.randomValue(-worldSize, worldSize))
         
         minDistance = 999999999
         for obj in self.world.all:
            distance = vectorMagnitude(vectorOffset( obj.position, newPosition))
            
            if distance < minDistance:
               minDistance = distance
         
         if minDistance > 500:
            return newPosition

   @Timing.timedFunction
   def tick(self):
      Cache.clear()
      self.world.simulate()

