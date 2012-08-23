

import math

import World
from Scalar import *
from Vector import *

class PointBody(World.WorldItem):
   def __init__(self, position):
      self.position = position
      self.velocity = [0, 0]

   def __eq__(self, rhs):
      return self is rhs
      
   def simulate(self):
      self.position = vectorAdd(self.position, self.velocity)
      
   def applyForce(self, force):
      acceleration = self.calculateDeltaVelocityDueToForce(force)
      self.velocity = vectorAdd(self.velocity, acceleration)
      
   def calculateDeltaVelocityDueToForce(self, force):
      deltaV = vectorScale(force, 1.0 / self.mass())
      
      return deltaV
      
   def mass(self):
      print "[PhysicsBody] Error: Mass Not Implemented"
      pass
      

class RigidBody(PointBody):
   def __init__(self, position):
      PointBody.__init__(self, position)
      
      self.rotation = math.pi/2
      self.spin = 0

   def simulate(self):
      PointBody.simulate(self)
      self.rotation = (self.rotation + self.spin) % (2 * math.pi)

   def applyLocalForce(self, force, atPoint=[0, 0]):
      force = vectorRotate(force, self.rotation)
      self.applyForce(force, atPoint)
   
   def applyForce(self, force, atPoint=[0,0]):
      PointBody.applyForce(self, force)
      
      self.spin += self.calculateDeltaSpinDueToForce(force, atPoint)
   
   def calculateDeltaSpinDueToForce(self, force, atPoint):
      localForce = vectorRotate(force, -self.rotation)
      return self.calculateDeltaSpinDueToLocalForce(localForce, atPoint)
   
   def calculateDeltaSpinDueToLocalForce(self, force, atPoint):
      dx, dy = atPoint
      tx, ty = force
      
      torque = (dx*ty - dy*tx)
      
      return torque / self.momentOfInertia()
