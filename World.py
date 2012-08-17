import random
import Vector

class World:
   def __init__(self):
      random.seed(500)
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
      combatTeams = []
      for a in self.all[:]:
         name = a.__class__.__name__
         
         if name == "Explosion":
            return True
            
         if name == "Ship":
            if not a.combatTeam in combatTeams:
               combatTeams.append(a)
               
            if len(combatTeams) > 1:
               return True
      
class WorldItem:
   destroyed = False
   combatTeam = -1
      
   def simulate(self):
      pass
      
   def solidFor(self, object):
      return True
      
   def seflectedBy(self, object):
      return True
