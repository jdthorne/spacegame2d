
import Scalar
import Vector

class EngineWrapper:
	def __init__(self, realEngine):
		self._engine = realEngine
	
	def Power(self):
		return self._engine.power
	def SetPower(self, power):
		self._engine.power = power
	
	def ThrustVector(self):
		return self._engine.thrustVector
		
	def Position(self):
		return self._engine.position
		
	def Dizzy(self):
		return self._engine.Dizzy()
		
	def Acceleration(self):
		return self._engine.Acceleration()

class TargetWrapper:
	def __init__(self, realShip, realTarget):
		self._ship = realShip
		self._target = realTarget
		
	def Vector(self):
		offset = Vector.Offset(self._target.position, self._ship.position)
		return Vector.Rotate(offset, -self._ship.rotation)

	def Velocity(self):
		relativeVelocity = Vector.Offset(self._target.velocity, self._ship.velocity)
		return Vector.Rotate(relativeVelocity, -self._ship.rotation)

class SensorWrapper:
	def __init__(self, realShip):
		self._ship = realShip
		
	def Scan(self):
		return [ TargetWrapper(self._ship, t) for t in self._ship.ScanForTargets() ]

class WeaponWrapper:
	def __init__(self, realWeapon):
		self._weapon = realWeapon
		
	def Fire(self):
		self._weapon.Fire()

class ShipWrapper:
	def __init__(self, realShip):
		self._ship = realShip
		self._engines = [ EngineWrapper(e) for e in self._ship.engines ]
		self._weapons = [ WeaponWrapper(w) for w in self._ship.weapons ]
		
	def Spin(self):
		return self._ship.spin
		
	def Velocity(self):
		return Vector.Rotate(self._ship.velocity, -self._ship.rotation)
	
	def Engines(self):
		return self._engines
		
	def Sensors(self):
		return SensorWrapper(self._ship)
		
	def Mass(self):
		return self._ship.Mass()
		
	def Weapons(self):
		return self._weapons
		