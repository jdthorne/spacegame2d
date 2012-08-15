

import math

import World
import Scalar
import Vector

class PointBody(World.WorldItem):
	def __init__(self, position):
		self.position = position
		self.velocity = [0, 0]
		
	def Simulate(self):
		self.position = Vector.Add(self.position, self.velocity)
		
	def ApplyForce(self, force):
		acceleration = self.CalculateDeltaVelocityDueToForce(force)
		self.velocity = Vector.Add(self.velocity, acceleration)
		
	def CalculateDeltaVelocityDueToForce(self, force):
		deltaV = Vector.Scale(force, 1.0 / self.Mass())
		
		return deltaV
		
	def Mass(self):
		print "[PhysicsBody] Error: Mass Not Implemented"
		pass
		

class RigidBody(PointBody):
	def __init__(self, position):
		PointBody.__init__(self, position)
		
		self.rotation = math.pi/2
		self.spin = 0

	def Simulate(self):
		PointBody.Simulate(self)
		self.rotation = (self.rotation + self.spin) % (2 * math.pi)
		
	# ============ FUNCTIONS YOU SHOULD REIMPLEMENT ==============
	def CenterOfMass(self):
		print "[PhysicsBody] Error: CenterOfMass Not Implemented"
		pass

	def MomentOfInertia(self):
		print "[PhysicsBody] Error: MomentOfInertia Not Implemented"
		pass


	# ========== APPLYING FORCES TO THIS BODY =============
	def ApplyLocalForce(self, force, atPoint=[0, 0]):
		force = Vector.Rotate(force, self.rotation)
		self.ApplyForce(force, atPoint)
	
	def ApplyForce(self, force, atPoint=[0,0]):
		PointBody.ApplyForce(self, force)
		
		self.spin += self.CalculateDeltaSpinDueToForce(force, atPoint)
	
	def CalculateDeltaSpinDueToForce(self, force, atPoint):
		localForce = Vector.Rotate(force, -self.rotation)
		return self.CalculateDeltaSpinDueToLocalForce(localForce, atPoint)
	
	def CalculateDeltaSpinDueToLocalForce(self, force, atPoint):
		dx, dy = Vector.Offset(self.CenterOfMass(), atPoint)
		tx, ty = force
		
		torque = -(dx*ty - dy*tx)
		
		return torque / self.MomentOfInertia()
