
import sys
import imp
import math
import World
import Ship
from Vector import *
import Cache
import Timing
import random

WORLD_SIZE = 9000

class Simulation:
   def __init__(self, fleets, seed):
      self.fleets = fleets
      self.seed = seed

      self.shipsToJump = []
      self.world = World.World(seed)

      i = 0
      for fleet in fleets:
         self.loadFleet(fleet, i)
         i += 1

      random.shuffle(self.shipsToJump)

   def complete(self):
      if len(self.shipsToJump) > 0:
         return False

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

      for name, design in fleet:
         self.loadShip(name, design, autopilot, fleetId)

   def loadShip(self, name, design, autopilot, fleetId):
      position = self.randomPosition()
      rotation = self.world.randomValue(0, 1000) * (math.pi / 1000.0)
      velocity = ( self.world.randomValue(-6.0, 6.0) , self.world.randomValue(-6.0, 6.0) )

      ship = Ship.Ship(name, design, autopilot, position, rotation, velocity, self.world, fleetId)
      self.world.prepareObject(ship)
      self.shipsToJump.append(ship)

   def randomPosition(self):
      while True:
         newPosition = (self.world.randomValue(-WORLD_SIZE, WORLD_SIZE), self.world.randomValue(-WORLD_SIZE, WORLD_SIZE))
         
         minDistance = 999999999
         for obj in self.world.all:
            distance = vectorMagnitude(vectorOffset( obj.position, newPosition))
            
            if distance < minDistance:
               minDistance = distance
         
         if minDistance > 5000:
            return newPosition

   @Timing.timedFunction
   def tick(self):
      if len(self.shipsToJump) > 0 and self.world.randomValue(0, 10) == 0:
         self.jumpNextShip()

      Cache.clear()
      self.world.simulate()

   def jumpNextShip(self):
      ship = self.shipsToJump[0]
      del self.shipsToJump[0]

      self.world.addObject(ship)


