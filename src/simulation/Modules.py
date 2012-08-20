from Vector import *
import Scalar
import ShipControls
import Misc
import Ship
import Timing
import Cache

class Module:
   isDeflector = False

   def __init__(self, parent, position, mass):
      self.parent = parent
      self.position = position
      self.mass = mass
 
   def absolutePosition(self):
      relativePosition = Vector.rotate(self.position, self.parent.rotation)
      return vectorAdd(relativePosition, self.parent.position)      

   def simulate(self):
      pass
      
class Structure(Module):
   def __init__(self, parent, position):
      Module.__init__(self, parent, position, 2)

class FlightComputer(Module):
   def __init__(self, parent, position, autopilot):
      Module.__init__(self, parent, position, 10)
 
      self.autopilot = None     
      self.createAutopilot = autopilot

   def simulate(self):
      if self.autopilot == None:
         self.autopilot = self.createAutopilot(ShipControls.ShipWrapper(self.parent))

      self.autopilot.run()

class Engine(Module):
   def __init__(self, parent, position, thrustVector):
      Module.__init__(self, parent, position, 3)
      
      self.thrustVector = thrustVector
      
      self.power = 0
      self.onTime = 0
      
   def currentThrust(self):
      return vectorScale(self.thrustVector, self.power)
      
   def simulate(self):
      self.power = Scalar.bound(0, self.power, 1)
   
      self.parent.applyLocalForce(self.currentThrust(), self.position)
      
   def dizzy(self):
      return self.parent.calculateDeltaSpinDueToLocalForce(self.thrustVector, self.position)
      
   def acceleration(self):
      return vectorScale(self.thrustVector, 1.0 / self.parent.mass())


class PlasmaCannon(Module):
   def __init__(self, parent, position):
      Module.__init__(self, parent, position, 5)
      self.recharge = 0
      
   def fire(self):
      if self.recharge > 0:
         return
         
      self.recharge = self.parent.world.randomValue(15, 45)
      
      bulletStart = vectorAdd(self.position, [1, 0])
      offset = Vector.rotate(bulletStart, self.parent.rotation)
      position = vectorAdd(self.parent.position, offset)
      
      self.parent.world.addObject(Misc.Bullet(position, Vector.rotate([Ship.MODULE_SIZE, 0], self.parent.rotation), self.parent))
   
   def simulate(self):
      if self.recharge > 0:
         self.recharge -= 1
         
class Deflector(Module):
   def __init__(self, parent, position):
      Module.__init__(self, parent, position, 15)

      self.isDeflector = True
   
   def simulate(self):
      powerupTime = 5.0 * 90.0

      self.parent.availableDeflectorPower = Scalar.bound(0.0, self.parent.availableDeflectorPower + 1.0/powerupTime, 1.0)

def simulateDeflectorsForShip(ship):
   range = 700.0

   totalDeflectors = 0
   for m in ship.modules:
      if m.isDeflector:
         totalDeflectors += 1

   for object in ship.world.all:
      if object is ship:
         continue
         
      if not object.solidFor(ship):
         continue
      
      distance = Vector.distance(object.position, ship.position)
      if distance < 1 or distance > range:
         continue

      power = (range - distance) / range
      power = power * power * ship.availableDeflectorPower * totalDeflectors

      mix = power
      object.velocity = vectorAdd(vectorScale(object.velocity, 1.0-mix), vectorScale(ship.velocity, mix))

      delta = vectorMagnitude(Vector.offset(object.velocity, ship.velocity))
      ship.availableDeflectorPower -= (power * delta * 0.004)
