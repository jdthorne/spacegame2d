
import math
import Vector

# Engine 0 = +1.0
# Engine 1 = -1.0

MAXIMUM_ROTATE_POWER = 0.75

def Sign(number):
	if number > 0:
		return 1
	if number < 0:
		return -1
		
	return 0

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
		
	def AngleSign(self, ship):
		return Sign(Vector.ShortestAngleBetween(ship.rotation, self.targetRotation))
		
	def Startup(self, ship):
		self.initialSign = self.AngleSign(ship)
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
		
		print "Engine power: %.3f  Delta Angle: %.3f" % (enginePower, deltaAngle)
		
		if self.AngleSign(ship) != self.initialSign:
			self.flightMode = self.Stabilize
			
		if enginePower < MAXIMUM_ROTATE_POWER / 2.0:
			enginePower = -MAXIMUM_ROTATE_POWER
		
		ship.engines[0].power = +(MAXIMUM_ROTATE_POWER * enginePower)
		ship.engines[1].power = -(MAXIMUM_ROTATE_POWER * enginePower)
		
	def Stabilize(self, ship):
		print "Stabilizing... %0.5f" % (ship.spin,)
		targetAcceleration = -ship.spin
		
		enginePower = targetAcceleration / MaximumDeltaSpin(ship.engines)
		ship.engines[0].power = +(MAXIMUM_ROTATE_POWER * enginePower)
		ship.engines[1].power = -(MAXIMUM_ROTATE_POWER * enginePower)
		
		if ship.spin < 0.0000001:
			self.flightMode = None


class Burn:
	def __init__(self, targetVelocity, nextFlightMode):
		self.targetVelocity = targetVelocity
		self.nextFlightMode = nextFlightMode
		
		self.lastDeltaV = 9999999
		
	def __call__(self, ship):
		print "Burning..."
		ship.engines[0].power = 1
		ship.engines[1].power = 1

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
		
	def CoastToBottom(self, ship):
		print "Coasting..."
		ship.engines[0].power = 0.0
		ship.engines[1].power = 0.0
		
		if ship.position[1] > 600:
			self.flightMode = self.TurnAtBottom
		
	def TurnAtBottom(self, ship):
		self.flightMode = RotateTo( math.pi, Burn([0, -2], self.CoastToTop) )

	def CoastToTop(self, ship):
		print "Coasting..."
		ship.engines[0].power = 0.0
		ship.engines[1].power = 0.0

		if ship.position[1] < 120:
			self.flightMode = self.TurnAtTop
		
	def TurnAtTop(self, ship):
		self.flightMode = RotateTo( 0, Burn([0, 2], self.CoastToBottom) )
		
