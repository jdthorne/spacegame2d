import random
import Event
from Vector import *

class World:
   def __init__(self, seed=500):
      random.seed(seed)

      self.size = 9000
      self.all = []
      self.combatTeams = []
      self.destroyedObjects = []

      self.onObjectAdded = Event.Event(self)
      self.onObjectRemoved = Event.Event(self)
      self.onUpdate = Event.Event(self)

   def setSeed(self, seed):
      random.seed(seed)

   def scan(self):
      results = []
      for team in self.combatTeams:
         results += team.activeShips()

      return results
      
   def addCombatTeam(self, team):
      self.combatTeams.append(team)

   def addObject(self, object):
      object.inWorld = True
      object.onDestroy += self.handleObjectDestroyed

      self.all.append(object)
      self.onObjectAdded(object)

   def removeObject(self, object):
      object.inWorld = False
      object.onDestroy -= self.handleObjectDestroyed

      self.all.remove(object)
      self.onObjectRemoved(object)

      object.onUpdate()
      
   def simulate(self):
      while len(self.destroyedObjects) > 0:
         self.removeObject(self.destroyedObjects.pop())

      for object in self.all:
         object.simulate()

      self.onUpdate()
      
   def randomValue(self, a, b):
      return random.randint(a, b)

   def handleObjectDestroyed(self, object):
      if not object in self.destroyedObjects:
         self.destroyedObjects.append(object)
      
class WorldItem:
   inWorld = False
   exciting = False
   life = 150

   def __init__(self):
      self.onUpdate = Event.Event(self)
      self.onDestroy = Event.Event(self)
      
   def simulate(self):
      pass
      
   def solidFor(self, object):
      return True

   def collide(self):
      self.destroy()
      
   def destroy(self):
      self.onDestroy()

