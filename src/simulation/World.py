import random
from Vector import *

class World:
   def __init__(self, seed=500):
      random.seed(seed)
      self.shipsToJump = []
      self.all = []
      self.combatants = []
      self.combatTeams = {}

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

      if object.combatTeam != -1:
         self.combatants.append(object)

      self.all.append(object)
      
   def simulate(self):
      if len(self.shipsToJump) > 0 and self.randomValue(0, 10) == 0:
         self.jumpNextShip()

      for object in self.all:
         if object.destroyed:
            self.all.remove(object)

            if object.combatTeam != -1:
               self.combatants.remove(object)
            
         else:
            object.simulate()
      
   def randomValue(self, a, b):
      return random.randint(a, b)
      
   def hasRemainingExcitement(self):
      for a in self.all[:]:
         if a.exciting:
            return True
      
      return False

      
class WorldItem:
   inWorld = False
   isShip = False
   exciting = False
   destroyed = False
   combatTeam = -1
   life = 150
      
   def simulate(self):
      pass
      
   def solidFor(self, object):
      return True
      
   def seflectedBy(self, object):
      return True
