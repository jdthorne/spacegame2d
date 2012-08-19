import random
import Vector

class World:
   def __init__(self, seed=500):
      random.seed(seed)
      self.all = []

   def scan(self):
      return self.all[:]
      
   def addObject(self, object):
      self.all.append(object)
      
   def simulate(self):
      for object in self.all[:]:
         if object.destroyed:
            self.all.remove(object)
            
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
   exciting = False
   destroyed = False
   combatTeam = -1
      
   def simulate(self):
      pass
      
   def solidFor(self, object):
      return True
      
   def seflectedBy(self, object):
      return True
