

import math

import World
import Scalar
import Vector
import Timing

class PointBody(World.WorldItem):
   def __init__(self, position):
      self.position = position
      self.velocity = [0, 0]
      
   @Timing.timedFunction("Physics/PointBody")
   def simulate(self):
      self.position = Vector.add(self.position, self.velocity)
      
   def applyForce(self, force):
      acceleration = self.calculateDeltaVelocityDueToForce(force)
      self.velocity = Vector.add(self.velocity, acceleration)
      
   def calculateDeltaVelocityDueToForce(self, force):
      deltaV = Vector.scale(force, 1.0 / self.mass())
      
      return deltaV
      
   def mass(self):
      print "[PhysicsBody] Error: Mass Not Implemented"
      pass
      

class RigidBody(PointBody):
   def __init__(self, position):
      PointBody.__init__(self, position)
      
      self.rotation = math.pi/2
      self.spin = 0

   @Timing.timedFunction("Physics/RigidBody")
   def simulate(self):
      PointBody.simulate(self)
      self.rotation = (self.rotation + self.spin) % (2 * math.pi)
      
   # ============ FUNCTIONS YOU SHOULD REIMPLEMENT ==============
   def centerOfMass(self):
      print "[PhysicsBody] Error: CenterOfMass Not Implemented"
      pass

   def momentOfInertia(self):
      print "[PhysicsBody] Error: MomentOfInertia Not Implemented"
      pass


   # ========== APPLYING FORCES TO THIS BODY =============
   def applyLocalForce(self, force, atPoint=[0, 0]):
      force = Vector.rotate(force, self.rotation)
      self.applyForce(force, atPoint)
   
   def applyForce(self, force, atPoint=[0,0]):
      PointBody.applyForce(self, force)
      
      self.spin += self.calculateDeltaSpinDueToForce(force, atPoint)
   
   def calculateDeltaSpinDueToForce(self, force, atPoint):
      localForce = Vector.rotate(force, -self.rotation)
      return self.calculateDeltaSpinDueToLocalForce(localForce, atPoint)
   
   def calculateDeltaSpinDueToLocalForce(self, force, atPoint):
      dx, dy = atPoint
      tx, ty = force
      
      torque = (dx*ty - dy*tx)
      
      return torque / self.momentOfInertia()
