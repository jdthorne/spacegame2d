
import sys
import imp
import math
import World
import Ship
from Vector import *
import Timing
import Fleet
import random
import Misc
import App

WORLD_SIZE = Misc.WEAPON_RANGE

class Simulation:
   def __init__(self, fleets, existingShips=[]):
      self.fleets = fleets

      teamId = 0
      for ship in existingShips:
         ship.world = App.world
         App.world.prepareObject(ship)
         App.world.addObject(ship)

      if len(existingShips) > 0:
         teamId = 1

      for fleet in fleets:
         fleet = Fleet.load(fleet)
         self.loadFleet(fleet, teamId)
         teamId += 1

      random.shuffle(App.world.shipsToJump)

   def complete(self):
      if len(App.world.shipsToJump) > 0:
         return False

      teams = []
      for o in App.world.all:
         if not o.combatTeam in teams:
            teams.append(o.combatTeam)

         if len(teams) > 1:
            return False

      return True

   def loadFleet(self, fleet, fleetId):
      for definition in fleet.ships:
         for i in range(definition.count):
            position = self.randomPosition()
            rotation = App.world.randomValue(0, 1000) * (math.pi / 1000.0)
            velocity = ( App.world.randomValue(-6.0, 6.0) , App.world.randomValue(-6.0, 6.0) )

            autopilot = self.loadAutopilot(definition.autopilot)

            ship = Ship.Ship(definition.name, definition.design, autopilot, position, rotation, velocity, App.world, fleetId)
            App.world.addToHyperspace(ship)

   def loadAutopilot(self, autopilotName):
      return imp.load_source(autopilotName, "./src/playerdata/autopilot/%s.py" % (autopilotName,)).Autopilot

   def randomPosition(self):
      while True:
         newPosition = (App.world.randomValue(-WORLD_SIZE, WORLD_SIZE), App.world.randomValue(-WORLD_SIZE, WORLD_SIZE))
         
         minDistance = 999999999
         for obj in App.world.all:
            distance = vectorMagnitude(vectorOffset( obj.position, newPosition))
            
            if distance < minDistance:
               minDistance = distance
         
         if minDistance > Misc.WEAPON_RANGE:
            return newPosition

   @Timing.timedFunction
   def tick(self):
      Cache.clear()
      App.world.simulate()


