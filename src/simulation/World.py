import random
import Event
from Vector import *

class World:
   def __init__(self, seed=500):
      random.seed(seed)
      self.shipsToJump = []
      self.all = []
      self.destroyed = []
      self.combatants = []
      self.combatTeams = {}

      self.onObjectAdded = Event.Event(self)
      self.onUpdate = Event.Event(self)

   def scan(self):
      return self.combatants
      
   def addToHyperspace(self, ship):
      self.prepareObject(ship)
      self.shipsToJump.append(ship)

   def jumpNextShip(self):
      ship = self.shipsToJump[0]
      del self.shipsToJump[0]

      self.addObject(ship)

   def prepareObject(self, object):
      if object.combatTeam != -1:
         if not object.combatTeam in self.combatTeams:
            self.combatTeams[object.combatTeam] = []

         self.combatTeams[object.combatTeam].append(object)

   def addObject(self, object):
      object.inWorld = True
      object.onDestroy += self.handleObjectDestroyed

      if object.combatTeam != -1:
         self.combatants.append(object)

      self.all.append(object)
      self.onObjectAdded(object)
      
   def simulate(self):
      if len(self.shipsToJump) > 0 and self.randomValue(0, 10) == 0:
         self.jumpNextShip()

      for object in self.destroyed:
         if object.combatTeam != -1:
            self.combatants.remove(object)

         self.all.remove(object)

      self.destroyed = []

      for object in self.all:
         object.simulate()

      self.onUpdate()
      
   def randomValue(self, a, b):
      return random.randint(a, b)

   def handleObjectDestroyed(self, object):
      self.destroyed.append(object)

      
class WorldItem:
   inWorld = False
   isShip = False
   exciting = False
   combatTeam = -1
   life = 150

   def __init__(self):
      self.onUpdate = Event.Event(self)
      self.onDestroy = Event.Event(self)
      
   def simulate(self):
      pass
      
   def solidFor(self, object):
      return True
      
   def destroy(self):
      self.onDestroy()

