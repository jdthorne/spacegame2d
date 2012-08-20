import Physics
import Scalar
from Vector import *

class Explosion(Physics.PointBody):
   def __init__(self, position, velocity, size):
      Physics.PointBody.__init__(self, position)
      
      self.exciting = True
      self.position = position
      self.velocity = velocity
      self.size = size
      
      self.initialLife = size
      self.life = size
   
   def simulate(self):
      Physics.PointBody.simulate(self)

      self.life -= 1
      
      if self.life < 5:
         self.destroyed = True
         
   def mass(self):
      return 5
      
   def solidFor(self, object):
      return False
      

class Bullet(Physics.PointBody):
   def __init__(self, position, velocity, owner):
      Physics.PointBody.__init__(self, position)
      
      self.deflectorHold = True
      self.velocity = velocity
      self.owner = owner
      
      self.initialLife = 50
      self.life = self.initialLife
      
   def mass(self):
      return 1.0
      
   def simulate(self):
      self.life -= 1
      Physics.PointBody.simulate(self)
      
      if Vector.distance(self.position, self.owner.position) >= 200:
         self.deflectorHold = False
         
      if self.life < 0:
         self.destroyed = True
      
   def solidFor(self, object):
      if object is self.owner:
         return False
      
      return True
