
import math

import Scalar
import Vector

MAXIMUM_ROTATE_POWER = 0.25
BURN_SPEED = 2.0

def EnginesFacing(engines, sign):
	return [e for e in engines if Scalar.Sign(e.DeltaSpinAtPower(MAXIMUM_ROTATE_POWER)) == sign]

def MaximumDeltaSpin(engines, sign):
	return Vector.Sum( [e.DeltaSpinAtPower(MAXIMUM_ROTATE_POWER) for e in EnginesFacing(engines, sign)] )

# Autopilot Library
class RotateTo:
	def __init__(self, targetRotation, nextFlightMode):
		self.targetRotation = targetRotation
		self.nextFlightMode = nextFlightMode
		
		self.flightMode = self.Startup
		
	def __call__(self, ship):
		if self.flightMode == None:
			return self.nextFlightMode
			
		self.flightMode(ship)
		
	def Startup(self, ship):
		self.flightMode = self.Rotate
		
	def Rotate(self, ship):
		deltaAngle = Vector.ShortestAngleBetween(ship.rotation, self.targetRotation)
		
		if deltaAngle == 0:
			self.flightMode = self.Stabilize
			return
		
		# Maxima - r = remaining rotation, a = acceleration, t = time, 
		#          s = spin, sf = final spin
		# 
		# solve( [ r = (1/2)*a*t^2 + s*t , sf = s + a*t ], [ a, t ]);
		# [[a = (sf^2-s^2)/(2*r), t = (2*r)/(sf+s)]]
		
		targetAcceleration = -(ship.spin**2) / (2*deltaAngle)
		
		enginePower = 0.0
		
		if abs(deltaAngle) > 1 and abs(targetAcceleration) == 0:
			# Kick the engine if necessary
			print "KICK"
			enginePower = 1.0
			
		else:
			maxRotate = MaximumDeltaSpin(ship.engines, -Scalar.Sign(targetAcceleration))			
			maxDerotate = MaximumDeltaSpin(ship.engines, Scalar.Sign(targetAcceleration))

			enginePower = -targetAcceleration / maxDerotate
		
			# Stabilize out if we're almost there
			if abs(deltaAngle) < abs(2 * ship.spin):
				self.flightMode = self.Stabilize
				return
				
			# Or: burn if we have a long ways to go
			elif abs(targetAcceleration) < abs(maxDerotate / 3):
				print "BURN"
				enginePower = -Scalar.Sign(enginePower)
				
			else:
				print "NORMAL"
		
		self.FireEngines(ship, enginePower)
		
		
	def Stabilize(self, ship):
		print "STABILIZE"
		targetAcceleration = -ship.spin
		
		if abs(targetAcceleration) < 0.00001:
			self.FireEngines(ship, 0.0)
			self.flightMode = None
			
		else:
			enginePower = -targetAcceleration / MaximumDeltaSpin(ship.engines, Scalar.Sign(targetAcceleration))
			
			self.FireEngines(ship, enginePower)
			
	def FireEngines(self, ship, power):
		enginesToFire = EnginesFacing(ship.engines, Scalar.Sign(power))
		for engine in ship.engines:
			if power != 0 and engine in enginesToFire:
				engine.power = +(abs(power) * MAXIMUM_ROTATE_POWER)
				
			else:
				engine.power = 0
		


class Burn:
	def __init__(self, engines, targetVelocity, nextFlightMode):
		self.engines = engines
		self.targetVelocity = targetVelocity
		self.nextFlightMode = nextFlightMode
		
		self.lastDeltaV = 9999999
		
	def __call__(self, ship):
	
		for engine in self.engines:
			engine.power = 1.0

		currentDeltaV = Vector.Magnitude(Vector.Offset(ship.velocity, self.targetVelocity))
		
		if currentDeltaV > self.lastDeltaV:
			return self.nextFlightMode
			
		self.lastDeltaV = currentDeltaV

class Autopilot:
	def __init__(self):
		self.flightMode = self.Startup
		
	def __call__(self, ship):
		nextMode = self.flightMode(ship)
		
		if nextMode != None:
			self.flightMode = nextMode
			
	def KillAllEngines(self, ship):
		for e in ship.engines:
			e.power = 0
		
	def Startup(self, ship):
		self.flightMode = self.TurnAtBottom
		
	def CoastToBottom(self, ship):
		self.KillAllEngines(ship)
		
		if ship.position[1] > 550:
			self.flightMode = self.TurnAtBottom
		
	def TurnAtBottom(self, ship):
		self.flightMode = RotateTo( 0, Burn(ship.thrustEngines, [0, -BURN_SPEED], self.CoastToTop) )

	def CoastToTop(self, ship):
		self.KillAllEngines(ship)

		if ship.position[1] < 170:
			self.flightMode = self.TurnAtTop
		
	def TurnAtTop(self, ship):
		self.flightMode = RotateTo( math.pi, Burn(ship.thrustEngines, [0, BURN_SPEED], self.CoastToBottom) )
		
