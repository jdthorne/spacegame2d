
import Scalar
import Vector

class EngineWrapper:
	def __init__(self, realEngine):
		self.__realEngine__ = realEngine
	
	def Power(self):
		return self.__realEngine__.power
	def SetPower(self, power):
		self.__realEngine__.power = power
	
	def ThrustVector(self):
		return self.__realEngine__.thrustVector
		
	def Position(self):
		return self.__realEngine__.position
		
	def DeltaSpinAtPower(self, power):
		return self.__realEngine__.DeltaSpinAtPower(power)

class TargetWrapper:
	def __init__(self, realShip, realTarget):
		self.__realShip__ = realShip
		self.__realTarget__ = realTarget
		
	def Vector(self):
		offset = Vector.Offset(self.__realShip__.position, self.__realTarget__.position)
		return Vector.Rotate(offset, self.__realShip__.rotation)

	def Velocity(self):
		relativeVelocity = Vector.Subtract(self.__realTarget__.velocity, self.__realShip__.velocity)
		return Vector.Rotate(relativeVelocity, self.__realShip__.rotation)

		
class SensorWrapper:
	def __init__(self, realShip):
		self.__realShip__ = realShip
		
	def Scan(self):
		return [ TargetWrapper(self.__realShip__, t) for t in self.__realShip__.ScanForTargets() ]

class ShipWrapper:
	def __init__(self, realShip):
		self.__realShip__ = realShip
		self.__engines__ = [ EngineWrapper(e) for e in self.__realShip__.engines ]
		
	def Spin(self):
		return self.__realShip__.spin
		
	def Velocity(self):
		return Vector.Rotate(self.__realShip__.velocity, -self.__realShip__.rotation)
	
	def Engines(self):
		return self.__engines__
		
	def Sensors(self):
		return SensorWrapper(self.__realShip__)