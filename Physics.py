
import Scalar
import Vector

class PhysicsBody:
	def __init__(self):
		self.position = [ 1280/2, 720/2 ]
		self.velocity = [ 0, 0 ]
		
		self.rotation = 0
		self.spin = 0.02
		
	# ============ FUNCTIONS YOU SHOULD REIMPLEMENT ==============
	def Mass(self):
		print "[PhysicsBody] Error: Mass Not Implemented"
		pass

	def CenterOfMass(self):
		print "[PhysicsBody] Error: CenterOfMass Not Implemented"
		pass

	def MomentOfInertia(self):
		print "[PhysicsBody] Error: MomentOfInertia Not Implemented"
		pass


	# ========== APPLYING FORCES TO THIS BODY =============
	def ApplyForce(self, force, atPoint):
		acceleration = self.CalculateDeltaVelocityDueToForce(force, atPoint)
		self.velocity = Vector.Add(self.velocity, acceleration)
								   
		self.spin += self.CalculateDeltaSpinDueToForce(force, atPoint)

	def CalculateDeltaVelocityDueToForce(self, force, atPoint):
		thrust = Vector.Rotate(force, self.rotation)
		deltaV = Vector.Scale(thrust, 1.0 / self.Mass())
		
		return deltaV
	
	def CalculateDeltaSpinDueToForce(self, force, atPoint):
		dx, dy = Vector.Offset(self.CenterOfMass(), atPoint)
		tx, ty = force
		
		torque = -(dx*ty - dy*tx)
		
		return torque / self.MomentOfInertia()

