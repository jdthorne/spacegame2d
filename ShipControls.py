
import Scalar
import Vector

class EngineWrapper:
   def __init__(self, realEngine):
      self._engine = realEngine
   
   def power(self):
      return self._engine.power
   def setPower(self, power):
      self._engine.power = power
   
   def thrustVector(self):
      return self._engine.thrustVector
      
   def position(self):
      return self._engine.position
      
   def dizzy(self):
      return self._engine.dizzy()
      
   def acceleration(self):
      return self._engine.acceleration()

class TargetWrapper:
   def __init__(self, realShip, realTarget):
      self._ship = realShip
      self._target = realTarget
      
   def vector(self):
      offset = Vector.offset(self._target.position, self._ship.position)
      return Vector.rotate(offset, -self._ship.rotation)

   def velocity(self):
      relativeVelocity = Vector.offset(self._target.velocity, self._ship.velocity)
      return Vector.rotate(relativeVelocity, -self._ship.rotation)
      
   def combatTeam(self):
      return self._target.combatTeam
      
   def destroyed(self):
      return self._target.distroyed

class SensorWrapper:
   def __init__(self, realShip):
      self._ship = realShip
      
   def scan(self):
      return [ TargetWrapper(self._ship, t) for t in self._ship.scanForTargets() ]

class WeaponWrapper:
   def __init__(self, realWeapon):
      self._weapon = realWeapon
      
   def fire(self):
      self._weapon.fire()

class ShipWrapper:
   def __init__(self, realShip):
      self._ship = realShip
      self._engines = [ EngineWrapper(e) for e in self._ship.engines ]
      self._weapons = [ WeaponWrapper(w) for w in self._ship.weapons ]
      
   def spin(self):
      return self._ship.spin
      
   def velocity(self):
      return Vector.Rotate(self._ship.velocity, -self._ship.rotation)
   
   def engines(self):
      return self._engines
      
   def sensors(self):
      return SensorWrapper(self._ship)
      
   def mass(self):
      return self._ship.mass()
      
   def weapons(self):
      return self._weapons
      
   def combatTeam(self):
      return self._ship.combatTeam
      
      
      
