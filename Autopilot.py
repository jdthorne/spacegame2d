
import math

import HUD
import Scalar
import Vector

def CalculatePowerLevelForSmoothApproach(distance, currentSpeed, maxPositiveAcceleration, maxNegativeAcceleration):
	if abs(distance) < 0.000001:
		return 0.0

	if abs(distance) < abs(currentSpeed * 4.0):
		return 0.0

	targetAcceleration = -(currentSpeed**2) / (2*distance)
	maxAppropriateAcceleration = maxNegativeAcceleration if distance < 0 else maxPositiveAcceleration
	maxAppropriateBraking = maxPositiveAcceleration if distance < 0 else maxNegativeAcceleration
	
	info = "[ Distance = %07.2f, Speed = %.5f, Target Acc = %.5f, Max Braking = %.5f ]" % (distance, currentSpeed, targetAcceleration, maxAppropriateBraking)

	# Moving away from the target - use full power towards it
	if Scalar.Sign(currentSpeed) != Scalar.Sign(distance):
		return 1.0 * Scalar.Sign(distance)
	
	# We have lots of time to brake, so let's accelerate instead
	elif abs(targetAcceleration) < abs(maxAppropriateBraking * 0.75):
		return 1.0 * Scalar.Sign(distance)
		
	# We should brake now!
	return abs(targetAcceleration / maxAppropriateBraking) * -Scalar.Sign(distance)
	
class Analysis:
	def __init__(self, ship):
		self.zeroDizzyEngines = [ e for e in ship.Engines() if e.Dizzy() == 0 ]
		self.positiveDizzyEngines = [ e for e in ship.Engines() if e.Dizzy() > 0 ]
		self.negativeDizzyEngines = [ e for e in ship.Engines() if e.Dizzy() < 0 ]
	
		self.maxPositiveDizzy = Vector.Sum([ e.Dizzy() for e in self.positiveDizzyEngines ])
		self.maxNegativeDizzy = Vector.Sum([ e.Dizzy() for e in self.positiveDizzyEngines ])
		
		self.forwardEngines = [ e for e in self.zeroDizzyEngines if e.ThrustVector()[0] > 0 ]
		self.reverseEngines = [ e for e in self.zeroDizzyEngines if e.ThrustVector()[0] < 0 ]
		
		self.maxForwardAcceleration = Vector.Sum([ e.Acceleration()[0] for e in self.forwardEngines ])
		self.maxReverseAcceleration = Vector.Sum([ e.Acceleration()[0] for e in self.reverseEngines ])
			
class Autopilot:
	def __init__(self, ship):
		self.target = None
		self.ship = ship
		
		self.analysis = Analysis(self.ship)
		
	def __call__(self):
		self.target = self.ship.Sensors().Scan()[0]
		self.RunAutopilot()
		
	def RunAutopilot(self):		
		self.ClearEngines()
		self.RotateToFaceTarget()
		
		self.ThrustToTargetRadius()
	
	def ClearEngines(self):
		for e in self.ship.Engines():
			e.SetPower(0)
			
	def PowerEngines(self, power, positiveEngines, negativeEngines):
		for e in positiveEngines:
			e.SetPower(power)
			
		for e in negativeEngines:
			e.SetPower(-power)

	def RotateToFaceTarget(self):
		angularDistance = Vector.Direction(self.target.Vector())
		angularSpeed = self.ship.Spin()
		
		power = CalculatePowerLevelForSmoothApproach(angularDistance, angularSpeed,
													 self.analysis.maxPositiveDizzy, 
											 	     self.analysis.maxNegativeDizzy)
 	     
		self.PowerEngines(power, self.analysis.positiveDizzyEngines, self.analysis.negativeDizzyEngines)
	
	
	def ThrustToTargetRadius(self):
		distance = Vector.Magnitude(self.target.Vector()) - 300
		speed = Vector.ScalarProjection(self.target.Velocity(), [0, 1])
		
		maxTowardAcceleration = Vector.ScalarProjection([0, self.analysis.maxForwardAcceleration], self.target.Vector())
		maxAwayAcceleration = Vector.ScalarProjection([0, self.analysis.maxForwardAcceleration], self.target.Vector())
		
		power = CalculatePowerLevelForSmoothApproach(distance, speed, maxTowardAcceleration, maxAwayAcceleration)

		self.PowerEngines(power, self.analysis.forwardEngines, self.analysis.reverseEngines)
			
		
		
