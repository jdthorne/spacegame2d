
import math

import Scalar
import Vector

MAXIMUM_ROTATE_POWER = 0.5
BURN_SPEED = 4.0

def EnginesFacing(engines, sign):
	return [e for e in engines if Scalar.Sign(e.DeltaSpinAtPower(MAXIMUM_ROTATE_POWER)) == sign]

def MaximumDeltaSpin(engines, sign):
	return Vector.Sum( [e.DeltaSpinAtPower(MAXIMUM_ROTATE_POWER) for e in EnginesFacing(engines, sign)] )

# Autopilot Library
class RotateTowards:
	def __init__(self, target, nextFlightMode):
		self.target = target
		self.nextFlightMode = nextFlightMode
		
		self.flightMode = self.Rotate
		
	def __call__(self, ship):
		if self.flightMode == None:
			return self.nextFlightMode
			
		self.flightMode(ship)
		
	def Rotate(self, ship):
		deltaAngle = Vector.Direction(Vector.Rotate(self.target.Vector(), math.pi/2))
		
		if deltaAngle == 0:
			self.flightMode = self.Stabilize
			return
		
		# Maxima - r = remaining rotation, a = acceleration, t = time, 
		#          s = spin, sf = final spin
		# 
		# solve( [ r = (1/2)*a*t^2 + s*t , sf = s + a*t ], [ a, t ]);
		# [[a = (sf^2-s^2)/(2*r), t = (2*r)/(sf+s)]]
		
		targetAcceleration = -(ship.Spin()**2) / (2*deltaAngle)
		
		enginePower = 0.0
		
		if abs(deltaAngle) > 1 and abs(targetAcceleration) == 0:
			# Kick the engine if necessary
			enginePower = 1.0
			
		elif abs(targetAcceleration) == 0:
			self.flightMode = self.Stabilize
			
		else:
			maxRotate = MaximumDeltaSpin(ship.Engines(), -Scalar.Sign(targetAcceleration))			
			maxDerotate = MaximumDeltaSpin(ship.Engines(), Scalar.Sign(targetAcceleration))

			enginePower = -targetAcceleration / maxDerotate
		
			# Stabilize out if we're almost there
			if abs(deltaAngle) < abs(2 * ship.Spin()):
				self.flightMode = self.Stabilize
				return
				
			# Or: burn if we have a long ways to go
			elif abs(targetAcceleration) < abs(maxDerotate / 3):
				enginePower = -Scalar.Sign(enginePower)
		
		self.FireEngines(ship, enginePower)
		
		
	def Stabilize(self, ship):
		print "STABILIZE"
		targetAcceleration = -ship.Spin()
		
		if abs(targetAcceleration) < 0.00001:
			self.FireEngines(ship, 0.0)
			self.flightMode = None
			
		else:
			enginePower = -targetAcceleration / MaximumDeltaSpin(ship.Engines(), Scalar.Sign(targetAcceleration))
			
			self.FireEngines(ship, enginePower)
			
	def FireEngines(self, ship, power):
		enginesToFire = EnginesFacing(ship.Engines(), Scalar.Sign(power))
		for engine in ship.Engines():
			if power != 0 and (engine in enginesToFire):
				engine.SetPower(abs(power) * MAXIMUM_ROTATE_POWER)
				
			else:
				engine.SetPower(0)
		


class Burn:
	def __init__(self, targetSpeed, nextFlightMode):
		self.targetSpeed = targetSpeed
		self.nextFlightMode = nextFlightMode
		
	def __call__(self, ship):
		speed = -ship.Velocity()[1]
		
		if abs(self.targetSpeed - speed) < 0.1:
			return self.nextFlightMode
			
		power = -Scalar.Sign(self.targetSpeed - speed)
		
		for engine in ship.Engines():
			if Scalar.Sign(engine.ThrustVector()[1]) == Scalar.Sign(power):
				engine.SetPower(1.0)
			else:
				engine.SetPower(0.0)

class Autopilot:
	def __init__(self):
		self.flightMode = Burn(1, self.AcquireTarget)
		self.target = None
		
	def __call__(self, ship):
		nextMode = self.flightMode(ship)
		
		if nextMode != None:
			self.flightMode = nextMode
		
	def AcquireTarget(self, ship):
		targets = ship.Sensors().Scan()
		
		self.target = targets[0]
		self.flightMode = self.Aim
		
	def Aim(self, ship):
		self.flightMode = RotateTowards(self.target, self.Burn)
		
	def Burn(self, ship):
		self.flightMode = Burn(1, self.Aim)
		
		
