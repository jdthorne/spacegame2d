
import math
import Vector

MAXIMUM_ROTATE_POWER = 0.25

def MaximumDeltaSpin(engines):
	return engines[0].DeltaSpinAtPower(MAXIMUM_ROTATE_POWER) + engines[1].DeltaSpinAtPower(-MAXIMUM_ROTATE_POWER)

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
		self.lastDeltaAngle = math.pi * 4
		self.flightMode = self.Rotate
		
	def Rotate(self, ship):
		deltaAngle = Vector.ShortestAngleBetween(ship.rotation, self.targetRotation)
		
		# Maxima - r = remaining rotation, a = acceleration, t = time, 
		#          s = spin, sf = final spin
		# 
		# solve( [ r = (1/2)*a*t^2 + s*t , sf = s + a*t ], [ a, t ]);
		# [[a = (sf^2-s^2)/(2*r), t = (2*r)/(sf+s)]]
		
		targetAcceleration = -(ship.spin**2) / (2*deltaAngle)
		
		enginePower = targetAcceleration / MaximumDeltaSpin(ship.engines)
		
		# Settle out if we're almost there
		if abs(deltaAngle) < abs(2 * ship.spin):
			self.flightMode = self.Stabilize
			
		# Or: burn if we have a long ways to go	
		elif abs(targetAcceleration) < abs(MaximumDeltaSpin(ship.engines) / 2):
			enginePower = Vector.Sign(deltaAngle)
		
		# Or: kick-start the engine if we're stuck
		elif abs(deltaAngle) > 3 and enginePower == 0:
			enginePower = 1.0

		print "Engine power: %.3f  Delta Angle: %.3f" % (enginePower, deltaAngle)
		
		ship.engines[0].power = +(enginePower * MAXIMUM_ROTATE_POWER)
		ship.engines[1].power = -(enginePower * MAXIMUM_ROTATE_POWER)
		self.lastDeltaAngle = deltaAngle
		
	def Stabilize(self, ship):
		print "Stabilizing... %0.5f" % (ship.spin,)
		targetAcceleration = -ship.spin
		
		enginePower = targetAcceleration / MaximumDeltaSpin(ship.engines)
		ship.engines[0].power = +(MAXIMUM_ROTATE_POWER * enginePower)
		ship.engines[1].power = -(MAXIMUM_ROTATE_POWER * enginePower)
		
		if abs(ship.spin) < 0.0000001:
			ship.engines[0].power = 0
			ship.engines[1].power = 0
			self.flightMode = None


class Burn:
	def __init__(self, targetVelocity, nextFlightMode):
		self.targetVelocity = targetVelocity
		self.nextFlightMode = nextFlightMode
		
		self.lastDeltaV = 9999999
		
	def __call__(self, ship):
	
		# Figure out how much spin each engine contributes
		safestEngine = None
		for engine in ship.engines:
			if safestEngine == None or abs(engine.DeltaSpinAtPower(1.0)) < abs(safestEngine.DeltaSpinAtPower(1.0)):
				safestEngine = engine

		# Now power each engine based on it's fraction of the spinniest
		for engine in ship.engines:
			fraction = abs(safestEngine.DeltaSpinAtPower(1.0)) / abs(engine.DeltaSpinAtPower(1.0))
			engine.power = fraction

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
		
	def Startup(self, ship):
		self.flightMode = self.TurnAtBottom
		# self.flightMode = Burn([0, 2], self.CoastToBottom)
		
	def CoastToBottom(self, ship):
		ship.engines[0].power = 0.0
		ship.engines[1].power = 0.0
		
		if ship.position[1] > 550:
			self.flightMode = self.TurnAtBottom
		
	def TurnAtBottom(self, ship):
		self.flightMode = RotateTo( math.pi, Burn([0, -2], self.CoastToTop) )

	def CoastToTop(self, ship):
		ship.engines[0].power = 0.0
		ship.engines[1].power = 0.0

		if ship.position[1] < 170:
			self.flightMode = self.TurnAtTop
		
	def TurnAtTop(self, ship):
		self.flightMode = RotateTo( 0, Burn([0, 2], self.CoastToBottom) )
		
